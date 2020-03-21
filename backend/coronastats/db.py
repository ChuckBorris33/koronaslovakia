import datetime
import typing

from peewee import SqliteDatabase, Model, DateField, AutoField, IntegerField

database = SqliteDatabase("../app.db")


class CoronaLog(Model):
    id = AutoField()
    datetime = DateField(default=datetime.date.today(), unique=True, index=True)
    infected = IntegerField(default=0)
    cured = IntegerField(default=0)
    tests = IntegerField(default=0)
    deaths = IntegerField(default=0)

    class Meta:
        database = database


def add_corona_log(infected: int, cured: int, tests: int, deaths: int = 0) -> CoronaLog:
    created = CoronaLog.create(infected=infected, cured=cured, tests=tests, deaths=deaths)
    return created


def get_infected_log() -> typing.Iterable[dict]:
    return CoronaLog.select(
        CoronaLog.datetime,
        CoronaLog.infected,
        CoronaLog.cured,
        CoronaLog.tests,
        CoronaLog.deaths,
    ).dicts()

