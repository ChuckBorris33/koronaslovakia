import datetime
import io
import csv
from collections import defaultdict

import click
import requests
from coronastats import db, scrapper, cache
from coronastats.scrapper import (
    get_corona_counts,
    get_location_data,
    get_korona_gov_data,
)
from coronastats import migrations

from flask import current_app

app = current_app


# Backup method for scrapping coronalog
@app.cli.command("backup_scrap_last_day_counts")
def backup_scrap_last_day_counts():
    get_corona_counts()


@click.option("--date", default=None, help="Date of log")
@app.cli.command("scrap_korona_gov_data")
def scrap_korona_gov_data(date=None):
    get_korona_gov_data(None, overwrite_updated_at=date)


@app.cli.command("scrap_location_counts")
def scrap_location_counts():
    get_location_data(always_update=True)


@app.cli.command("edit_log")
@click.option("--date", default=None, help="Date of log")
@click.option("-i", "--infected", default=None, help="Number of infected.")
@click.option("-t", "--tests", default=None, help="Number of tests.")
@click.option("-c", "--cured", default=None, help="Number of cured.")
@click.option("-d", "--deaths", default=None, help="Number of deaths.")
@click.option("-m", "--median", default=None, help="Median number.")
def edit_log(
    date=None, infected=None, tests=None, cured=None, deaths=None, median=None
):
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
    if median:
        log.median = median
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


@app.cli.command("load_vaccinated")
def load_vaccinated():
    result = requests.get(
        "https://raw.githubusercontent.com/Institut-Zdravotnych-Analyz/covid19-data/"
        + "main/Vaccination/OpenData_Slovakia_Vaccination_Regions.csv"
    )
    csv_stream = io.StringIO(result.text)
    reader = csv.DictReader(csv_stream, delimiter=";")
    date_data = defaultdict(dict)
    last_row = None
    for row in reversed(list(reader)):
        date = datetime.datetime.strptime(row["Date"], "%Y-%m-%d").date()
        if last_row and "vaccinated" not in date_data[date]:
            date_data[date]["vaccinated"] = last_row["vaccinated"]
            date_data[date]["vaccinated_2nd_dose"] = last_row["vaccinated_2nd_dose"]
        date_data[date]["vaccinated"] = date_data[date].get("vaccinated", 0) + int(
            row["first_dose"]
        )
        date_data[date]["vaccinated_2nd_dose"] = date_data[date].get(
            "vaccinated_2nd_dose", 0
        ) + int(row["second_dose"])
        last_row = date_data[date]
    logs = db.CoronaLog.select().where(db.CoronaLog.date.in_(list(date_data.keys())))
    to_update = []
    for log in logs.iterator():
        new_vaccinated = date_data[log.date]["vaccinated"]
        new_vaccinated_2nd_dose = date_data[log.date]["vaccinated_2nd_dose"]
        if (
            new_vaccinated != log.vaccinated
            or new_vaccinated_2nd_dose != log.vaccinated_2nd_dose
        ):
            log.vaccinated = date_data[log.date]["vaccinated"]
            log.vaccinated_2nd_dose = date_data[log.date]["vaccinated_2nd_dose"]
            to_update.append(log)
    db.CoronaLog.bulk_update(
        to_update, fields=[db.CoronaLog.vaccinated, db.CoronaLog.vaccinated_2nd_dose]
    )
