import datetime

from coronastats.cache import clear_cache
from flask_script import Manager

from coronastats import db
from coronastats.server import create_app
from coronastats.scrapper import get_corona_counts

manager = Manager(create_app)


@manager.command
def prepare_database():
    db.database.create_tables([db.CoronaLog])


@manager.command
def add_initial_data():
    data = [
        (datetime.datetime(2020, 3, 6), 1, 306),
        (datetime.datetime(2020, 3, 7), 3, 392),
        (datetime.datetime(2020, 3, 8), 5, 496),
        (datetime.datetime(2020, 3, 9), 7, 548),
        (datetime.datetime(2020, 3, 10), 7, 590),
        (datetime.datetime(2020, 3, 11), 10, 713),
        (datetime.datetime(2020, 3, 12), 21, 853),
        (datetime.datetime(2020, 3, 13), 32, 1006),
        (datetime.datetime(2020, 3, 14), 44, 1147 + 44),
        (datetime.datetime(2020, 3, 15), 61, 1375 + 61),
        (datetime.datetime(2020, 3, 16), 72, 1523 + 72),
        (datetime.datetime(2020, 3, 17), 97, 1816 + 97),
        (datetime.datetime(2020, 3, 18), 105, 2033 + 105),
        (datetime.datetime(2020, 3, 19), 124, 2406 + 124),
        (datetime.datetime(2020, 3, 20), 137, 2707),
    ]
    fields = [db.CoronaLog.datetime, db.CoronaLog.infected, db.CoronaLog.tests]
    with db.database.atomic():
        db.CoronaLog.insert_many(data, fields=fields).execute()


@manager.command
def scrap_last_day_counts():
    last_date = db.get_last_log_date()
    get_corona_counts(last_date)


@manager.command
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
    clear_cache()


if __name__ == "__main__":
    manager.run()
