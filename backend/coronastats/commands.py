import datetime

import click
from coronastats import db, scrapper, cache
from coronastats.scrapper import get_corona_counts, get_location_data, get_korona_gov_data
from coronastats import migrations

from flask import current_app

app = current_app


#Backup method for scrapping coronalog
@app.cli.command("backup_scrap_last_day_counts")
def backup_scrap_last_day_counts():
    get_corona_counts()


@app.cli.command("scrap_korona_gov_data")
def scrap_korona_gov_data():
    get_korona_gov_data()


@app.cli.command("scrap_location_counts")
def scrap_location_counts():
    get_location_data(always_update=True)


@app.cli.command("edit_log")
@click.option("--date", default=None, help="Date of log")
@click.option("-i", "--infected", default=None, help="Number of infected.")
@click.option("-t", "--tests", default=None, help="Number of tests.")
@click.option("-c", "--cured", default=None, help="Number of cured.")
@click.option("-d", "--deaths", default=None, help="Number of deaths.")
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


@app.cli.command("migrate")
@click.argument("goal_version", default=len(migrations.migrations))
def migrate(goal_version):
    migrations.run_migrations(goal_version)


@app.cli.command("show_migrations")
def show_migrations():
    migrations.show_migrations()


@app.cli.command("set_migration_state")
@click.argument("version")
def set_migration_state(version):
    return migrations.set_migration_state(version)
