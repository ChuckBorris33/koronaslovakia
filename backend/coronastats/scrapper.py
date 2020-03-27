import json
import logging
import os
import sys
import time
from datetime import date, datetime

import requests
import schedule

from coronastats import db
from coronastats.cache import clear_cache

logger = logging.getLogger()
logger.setLevel(os.getenv("LOGLEVEL", logging.INFO))
ch = logging.StreamHandler()
ch.setLevel(os.getenv("LOGLEVEL", logging.INFO))
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


def get_corona_counts(last_date: date):
    try:
        logger.info(f"Trying to scrap new corona stats")
        result = requests.get("https://virus-korona.sk/api.php")
        if result.status_code != 200:
            raise ConnectionError(
                "Unable to fetch data from https://virus-korona.sk/api.php"
            )
        data = json.loads(result.text)
        infected_data = data["tiles"]["k26"]["data"]["d"].pop()
        tested_data = data["tiles"]["k25"]["data"]["d"].pop()
        cured_data = data["tiles"]["k34"]["data"]["d"].pop()
        deaths_data = data["tiles"]["k35"]["data"]["d"].pop()
        updated_at = datetime.strptime(infected_data["d"], "%y%m%d").date()
        if updated_at > last_date:
            infected = int(infected_data["v"])
            tested = int(tested_data["v"]) + infected
            cured = int(cured_data["v"])
            deaths = int(deaths_data["v"])
            db.add_corona_log(
                infected=infected,
                cured=cured,
                tests=tested,
                deaths=deaths,
                date_=updated_at,
            )
            clear_cache()
            logger.info(f"Scrapped {infected}, {tested}, Cancelling job for today")
            return schedule.CancelJob
        else:
            logger.info(f"Stats not updated")
    except Exception as error:
        logger.error(str(error))
        return schedule.CancelJob


def start_trying_to_get_corona_counts():
    try:
        last_date = db.get_last_log_date()
        schedule.every(10).minutes.do(get_corona_counts, last_date)
    except Exception as error:
        logger.error(str(error))
        raise


if __name__ == "__main__":
    schedule.every().day.at("09:00").do(start_trying_to_get_corona_counts)
    logging.info("Coronastat scrapper started")
    while True:
        try:
            schedule.run_pending()
            time.sleep(30)
        except KeyboardInterrupt:
            sys.exit()
