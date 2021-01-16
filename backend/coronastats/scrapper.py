import json
import re
import sys
import time
import typing
from datetime import date, datetime, timedelta

import coronastats
import requests
import schedule

from bs4 import BeautifulSoup, Comment, PageElement
from flask import current_app

from coronastats import db, cache

logger = current_app.logger.getChild("scrapper")


def _normalize_number(number: str, default: int = 0) -> int:
    if not number:
        return default
    try:
        return int(re.sub("[^0-9]+", "", number))
    except ValueError:
        pass
    return default


def _find_comment(text: Comment, comment: str) -> PageElement:
    clean_text = str(text).strip()
    return isinstance(text, Comment) and clean_text == comment


def get_element_with_comment(container: PageElement, comment: str) -> PageElement:
    return container.find(text=lambda t: _find_comment(t, comment)).find_parent()


def get_korona_gov_data(
    last_date: typing.Optional[date] = None,
    overwrite_updated_at: typing.Optional[date] = None,
):
    try:
        result = requests.get(
            "https://korona.gov.sk/koronavirus-na-slovensku-v-cislach/"
        )
        if result.status_code != 200:
            raise ConnectionError(
                "Unable to fetch data from "
                + "https://korona.gov.sk/koronavirus-na-slovensku-v-cislach/"
            )
        wrapper = BeautifulSoup(result.text, "html.parser")
        c = wrapper.find("main").findAll("div", {"class": "govuk-width-container"})[1]
        date_text = get_element_with_comment(c, "REPLACE:koronastats-last-update").text
        updated_at = overwrite_updated_at or (
            datetime.strptime(date_text, "Aktualizované %d. %m. %Y").date()
            - timedelta(days=1)
        )

        last_log = db.get_last_log()

        if last_date is None or updated_at > last_date:
            infected = _normalize_number(
                get_element_with_comment(c, "REPLACE:koronastats-positives").text,
                last_log.infected,
            )
            tested = _normalize_number(
                get_element_with_comment(c, "REPLACE:koronastats-lab-tests").text,
                last_log.tests,
            )
            cured = _normalize_number(
                get_element_with_comment(c, "REPLACE:koronastats-cured").text,
                last_log.cured,
            )
            deaths = _normalize_number(
                get_element_with_comment(c, "REPLACE:koronastats-deceased").text,
                last_log.deaths,
            )
            median = _normalize_number(
                get_element_with_comment(c, "REPLACE:koronastats-median").text,
                last_log.median,
            )
            hospitalized = _normalize_number(
                get_element_with_comment(c, "REPLACE:koronastats-hospitalized").text,
                last_log.hospitalized,
            )
            confirmed_hospitalized = _normalize_number(
                get_element_with_comment(
                    c, "REPLACE:koronastats-hospitalized-covid19"
                ).text,
                last_log.confirmed_hospitalized,
            )
            ag_tests = _normalize_number(
                get_element_with_comment(
                    c, "REPLACE:koronastats-ag-tests"
                ).text,
                last_log.ag_tests,
            )
            ag_positive = _normalize_number(
                get_element_with_comment(
                    c, "REPLACE:koronastats-ag-positives"
                ).text,
                last_log.ag_positive,
            )
            confirmed_hospitalized_text = get_element_with_comment(
                c, "REPLACE:koronastats-hospitalized-covid19-intensive"
            ).text
            confirmed_hospitalized_text_match = re.match(
                (
                    r"Počet hospitalizovanýchs potvrdeným covid19z toho na "
                    r"JIS: (.+) a na pľúcnej ventilácii: (.+)"
                ),
                confirmed_hospitalized_text,
            )
            confirmed_hospitalized_icu = _normalize_number(
                confirmed_hospitalized_text_match.group(1)
                if confirmed_hospitalized_text_match
                else 0,
                last_log.confirmed_hospitalized_icu,
            )
            confirmed_hospitalized_ventilation = _normalize_number(
                confirmed_hospitalized_text_match.group(2)
                if confirmed_hospitalized_text_match
                else 0,
                last_log.confirmed_hospitalized_ventilation,
            )
            try:
                vacinated_label = wrapper.find('strong', text = re.compile('Počet zaočkovaných'))
                vaccinated = _normalize_number(vacinated_label.find_parent().find_parent().h3.text, last_log.vaccinated)
            except:
                vaccinated = last_log.vaccinated
            db.add_corona_log(
                infected=infected,
                cured=cured,
                tests=tested,
                deaths=deaths,
                log_date=updated_at,
                median=median,
                hospitalized=hospitalized,
                confirmed_hospitalized=confirmed_hospitalized,
                confirmed_hospitalized_icu=confirmed_hospitalized_icu,
                confirmed_hospitalized_ventilation=confirmed_hospitalized_ventilation,
                vaccinated=vaccinated,
                ag_tests=ag_tests,
                ag_positive=ag_positive,
            )
            cache.clear()
            if last_date is not None and updated_at > last_date:
                logger.info(f"Scrapped {infected}, {tested}, Cancelling job for today")
                return schedule.CancelJob

    except Exception:
        logger.exception("Error while scrapping data")
        return schedule.CancelJob


# Old scrapper method kept as backup
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
            logger.info("Stats not updated")
    except Exception:
        logger.exception("Error while scrapping data")
        return schedule.CancelJob


def _normalize_location_title(title: str) -> str:
    if title in (
        "Bratislava I",
        "Bratislava II",
        "Bratislava III",
        "Bratislava IV",
        "Bratislava V",
    ):
        return "Bratislava"
    elif title in ("Košice I", "Košice II", "Košice III", "Košice IV"):
        return "Košice"
    return title


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
        map_data = json.loads(result.text)["districts"]
        is_updated = False
        location_map = {
            location.location: location for location in db.CoronaLocation.select()
        }
        for record in map_data:
            title = _normalize_location_title(record["title"])
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
                    title = _normalize_location_title(record["title"])
                    location = location_map[title]

                    location_log, _ = db.CoronaLocationLog.get_or_create(
                        location=location, date=datetime.today()
                    )
                    location_log.infected = record["amount"]["infected"]
                    location_log.cured = record["amount"]["recovered"]
                    location_log.deaths = record["amount"]["deaths"]
                    location_log.save()
            logger.info("Updated location data")
        cache.clear()
    except Exception:
        logger.exception("Error while scrapping data")
        return schedule.CancelJob


def start_trying_to_get_korona_gov_data():
    try:
        last_date = db.get_last_log_date()
        schedule.every(10).minutes.do(get_korona_gov_data, last_date)
    except Exception as error:
        logger.error(str(error))
        raise


def run():
    schedule.every().day.at("09:00").do(start_trying_to_get_korona_gov_data)
    schedule.every().hour.do(get_location_data)
    schedule.every().day.at("23:30").do(get_location_data, always_update=True)
    logger.info("Coronastat scrapper started")
    while True:
        try:
            schedule.run_pending()
            time.sleep(30)
        except KeyboardInterrupt:
            sys.exit()
