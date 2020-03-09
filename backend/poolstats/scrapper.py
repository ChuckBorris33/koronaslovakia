import time
import sys

import requests
import schedule
from bs4 import BeautifulSoup

from poolstats import db


def get_and_store_visitor_count():
    try:
        result = requests.get("https://petrzalka.sk/plavaren/")
        if result.status_code != 200:
            return None
        soup = BeautifulSoup(result.text, "html.parser")
        visitor_count = soup.find("span", class_="szp-occupancy").string
        db.add_visitor_log(visitor_count)
    except Exception:
        pass


if __name__ == "__main__":
    schedule.every(5).minutes.do(get_and_store_visitor_count)
    print("Poolstat scrapper started")
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            sys.exit()

