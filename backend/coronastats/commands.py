import datetime

from coronastats import db, scrapper, cache
from coronastats.scrapper import get_corona_counts
from flask import current_app

app = current_app


@app.cli.command("prepare_database")
def prepare_database():
    db.database.create_tables([db.CoronaLog])


@app.cli.command("scrap_last_day_counts")
def scrap_last_day_counts():
    last_date = db.get_last_log_date()
    get_corona_counts(last_date)


@app.cli.command("edit_log")
def edit_log(date=None, infected=None, tests=None, cured=None, killed=None):
    log_date = (
        datetime.datetime.strptime(date, "%Y-%m-%d").date()
        if date
        else db.get_last_log_date()
    )
    log, created = db.get_log_by_date(log_date)
    if infected:
        log.infected = infected
    if tests:
        log.tests = tests
    if cured:
        log.cured = cured
    if killed:
        log.deaths = killed
    log.save()
    cache.clear()


@app.cli.command("scrapper")
def run_scrapper():
    scrapper.run()

