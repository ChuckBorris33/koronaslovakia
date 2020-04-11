import datetime

import click
from coronastats import db, scrapper, cache
from coronastats.scrapper import get_corona_counts, get_location_data
from flask import current_app

app = current_app


@app.cli.command("prepare_database")
def prepare_database():
    db.database.create_tables([db.CoronaLog])


@app.cli.command("prepare_location_database")
def prepare_location_database():
    db.database.create_tables([db.CoronaLocationLog, db.CoronaLocation])


@app.cli.command("scrap_last_day_counts")
def scrap_last_day_counts():
    get_corona_counts()


@app.cli.command("scrap_location_counts")
def scrap_location_counts():
    get_location_data(always_update=True)


@app.cli.command("edit_log")
@click.option('--date', default=None, help='Date of log')
@click.option('-i', '--infected', default=None, help='Number of infected.')
@click.option('-t', '--tests', default=None, help='Number of tests.')
@click.option('-c', '--cured', default=None, help='Number of cured.')
@click.option('-d', '--deaths', default=None, help='Number of deaths.')
def edit_log(date=None, infected=None, tests=None, cured=None, deaths=None):
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
    if deaths:
        log.deaths = deaths
    log.save()
    cache.clear()


@app.cli.command("scrapper")
def run_scrapper():
    scrapper.run()

