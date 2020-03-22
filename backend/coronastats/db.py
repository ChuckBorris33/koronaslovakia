import datetime
import typing

from peewee import SqliteDatabase, Model, DateField, AutoField, IntegerField, JOIN, fn, Value

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
    created = CoronaLog.insert(
        infected=infected, cured=cured, tests=tests, deaths=deaths
    ).on_conflict_replace().execute()
    return created


def get_infected_log() -> typing.Iterable[dict]:
    return CoronaLog.select(
        CoronaLog.datetime,
        CoronaLog.infected,
        CoronaLog.cured,
        CoronaLog.tests,
        CoronaLog.deaths,
    ).dicts()


def get_infected_increase_log() -> typing.Iterable[dict]:
    CoronaLogPrevieous = CoronaLog.alias()
    previous_query = CoronaLogPrevieous.select()
    previous_query = previous_query.alias("clp")

    return (
        CoronaLog.select(
            CoronaLog.datetime,
            Value(CoronaLog.infected - fn.COALESCE(previous_query.c.infected, 0)).alias("infected_increase"),
            Value(CoronaLog.cured - fn.COALESCE(previous_query.c.cured, 0)).alias("cured_increase"),
            Value(CoronaLog.tests - fn.COALESCE(previous_query.c.tests, 0)).alias("tests_increase"),
            Value(CoronaLog.deaths - fn.COALESCE(previous_query.c.deaths, 0)).alias("deaths_increase"),
        )
        .join(
            previous_query,
            JOIN.LEFT_OUTER,
            on=(previous_query.c.id == CoronaLog.id - 1),
        )
        .dicts()
    )
