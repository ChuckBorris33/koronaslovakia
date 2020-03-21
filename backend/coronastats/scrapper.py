import logging
import time
import sys

import requests
import schedule
from bs4 import BeautifulSoup

from coronastats import db

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)

def get_corona_counts():
    try:
        result = requests.get("https://www.korona.gov.sk/")
        if result.status_code != 200:
            raise ConnectionError("Unable to fetch data from https://www.korona.gov.sk/")
        soup = BeautifulSoup(result.text, "html.parser")
        counters = soup.find("div", class_="covd-counter").find_all("div")
        infected, tested = 0, 0
        for counter in counters:
            title = counter.find("span", class_="countTitle").text
            if title == "Testovaných":
                tested = int(counter.find("span", class_="countValue").string)
            elif title == "Pozitívnych":
                infected = int(counter.find("span", class_="countValue").string)
        db.add_corona_log(infected=infected, cured=0, tests=tested, deaths=0)
        logger.info(f"Scrapped {infected}, {tested}")
    except Exception as error:
        logger.error(str(error))


if __name__ == "__main__":
    schedule.every().day.at("18:00").do(get_corona_counts)
    logger.info("Coronastat scrapper started")
    while True:
        try:
            schedule.run_pending()
            time.sleep(1000)
        except KeyboardInterrupt:
            sys.exit()

