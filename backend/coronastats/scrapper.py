import json
import sys
import time
import typing
from datetime import date, datetime

import coronastats
import requests
import schedule

from coronastats import db, cache
from flask import current_app

logger = current_app.logger.getChild("scrapper")


def get_corona_counts(last_date: typing.Optional[date] = None):
    try:
        result = requests.get("https://virus-korona.sk/api.php")
        if result.status_code != 200:
            raise ConnectionError(
                "Unable to fetch data from https://virus-korona.sk/api.php"
            )
        data = json.loads(result.text)
        infected_data = data["tiles"]["k5"]["data"]["d"].pop()
        tested_data = data["tiles"]["k23"]["data"]["d"].pop()
        cured_data = data["tiles"]["k7"]["data"]["d"].pop()
        deaths_data = data["tiles"]["k8"]["data"]["d"].pop()
        updated_at = datetime.strptime(infected_data["d"], "%y%m%d").date()
        if last_date is None or updated_at > last_date:
            infected = int(infected_data["v"])
            tested = int(tested_data["v"])
            cured = int(cured_data["v"])
            deaths = int(deaths_data["v"])
            db.add_corona_log(
                infected=infected,
                cured=cured,
                tests=tested,
                deaths=deaths,
                log_date=updated_at,
            )
            cache.clear()
            if last_date is not None and updated_at > last_date:
                logger.info(f"Scrapped {infected}, {tested}, Cancelling job for today")
                return schedule.CancelJob
        else:
            logger.info(f"Stats not updated")
    except Exception:
        logger.exception("Error while scrapping data")
        return schedule.CancelJob


def _get_or_create_location(
    title: str, location_map: dict
) -> typing.Tuple[db.CoronaLocation, bool]:
    if title in location_map:
        return location_map[title], False
    else:
        return db.CoronaLocation.create(location=title), True


def get_location_data(always_update: bool = False):
    try:
        result = requests.get("https://mapa.covid.chat/map_data")
        if result.status_code != 200:
            raise ConnectionError(
                "Unable to fetch data from https://mapa.covid.chat/map_data"
            )
        map_data = json.loads(result.text)["map"]
        is_updated = False
        location_map = {
            location.location: location for location in db.CoronaLocation.select()
        }
        for record in map_data:
            title = record["title"]
            location, created = _get_or_create_location(title, location_map)
            last_updated = datetime.fromtimestamp(
                int(record["last_occurrence_timestamp"])
            ).date()
            if created or last_updated > location.last_updated:
                location_map[title] = location
                location.last_updated = last_updated
                location.save()
                is_updated = True
        if always_update or is_updated:
            with coronastats.db_wrapper.database.atomic():
                for record in map_data:
                    title = record["title"]
                    location = location_map[title]

                    location_log, _ = db.CoronaLocationLog.get_or_create(
                        location=location, date=datetime.today()
                    )
                    location_log.infected = record["amount"]["infected"]
                    location_log.infected_females = record["females"]
                    location_log.cured = record["amount"]["recovered"]
                    location_log.deaths = record["amount"]["deaths"]
                    location_log.save()
            logger.info("Updated location data")
        cache.clear()
    except Exception:
        logger.exception("Error while scrapping data")
        return schedule.CancelJob


def start_trying_to_get_corona_counts():
    try:
        last_date = db.get_last_log_date()
        schedule.every(10).minutes.do(get_corona_counts, last_date)
    except Exception as error:
        logger.error(str(error))
        raise


def run():
    schedule.every().day.at("09:00").do(start_trying_to_get_corona_counts)
    schedule.every().hour.do(get_location_data)
    schedule.every().day.at("23:30").do(get_location_data, always_update=True)
    logger.info("Coronastat scrapper started")
    while True:
        try:
            schedule.run_pending()
            time.sleep(30)
        except KeyboardInterrupt:
            sys.exit()
