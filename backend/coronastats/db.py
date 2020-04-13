import datetime
import typing

from coronastats import db_wrapper
from peewee import (
    DateField,
    AutoField,
    IntegerField,
    JOIN,
    fn,
    Value,
    CharField,
    ForeignKeyField,
)
from playhouse.shortcuts import model_to_dict


class CoronaLog(db_wrapper.Model):
    id = AutoField()
    datetime = DateField(default=datetime.date.today(), unique=True, index=True)
    infected = IntegerField(default=0)
    cured = IntegerField(default=0)
    tests = IntegerField(default=0)
    deaths = IntegerField(default=0)


class CoronaLocation(db_wrapper.Model):
    id = AutoField()
    location = CharField(index=True)
    last_updated = DateField(default=datetime.date.today())


class CoronaLocationLog(db_wrapper.Model):
    id = AutoField()
    date = DateField(default=datetime.date.today(), index=True)
    infected = IntegerField(default=0)
    infected_females = IntegerField(default=0)
    cured = IntegerField(default=0)
    tests = IntegerField(default=0)
    deaths = IntegerField(default=0)
    location = ForeignKeyField(CoronaLocation, backref="data")


def add_corona_log(
    infected: int,
    cured: int,
    tests: int,
    deaths: int = 0,
    date_: typing.Optional[datetime.date] = None,
) -> int:
    if not date_:
        date_ = datetime.date.today()
    created_id = (
        CoronaLog.insert(
            infected=infected, cured=cured, tests=tests, deaths=deaths, datetime=date_
        )
        .on_conflict(
            conflict_target=[CoronaLog.datetime],
            preserve=[
                CoronaLog.infected,
                CoronaLog.cured,
                CoronaLog.tests,
                CoronaLog.deaths,
            ],
        )
        .execute()
    )
    return created_id


def get_log_by_date(log_date):
    return CoronaLog.get_or_create(datetime=log_date)


def get_last_log_date() -> datetime.date:
    return (
        CoronaLog.select(CoronaLog.datetime)
        .order_by(CoronaLog.datetime.desc())
        .get()
        .datetime
    )


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
            Value(CoronaLog.infected - fn.COALESCE(previous_query.c.infected, 0)).alias(
                "infected_increase"
            ),
            Value(CoronaLog.cured - fn.COALESCE(previous_query.c.cured, 0)).alias(
                "cured_increase"
            ),
            Value(CoronaLog.tests - fn.COALESCE(previous_query.c.tests, 0)).alias(
                "tests_increase"
            ),
            Value(CoronaLog.deaths - fn.COALESCE(previous_query.c.deaths, 0)).alias(
                "deaths_increase"
            ),
        )
        .join(
            previous_query,
            JOIN.LEFT_OUTER,
            on=(previous_query.c.id == CoronaLog.id - 1),
        )
        .dicts()
    )


def get_last_log_by_location():
    results = []
    day_before_yesterday = datetime.date.today() - datetime.timedelta(days=2)
    query = CoronaLocation.select().prefetch(
        CoronaLocationLog.select()
        .order_by(CoronaLocationLog.date.desc())
        .where(CoronaLocationLog.date >= day_before_yesterday)
    )
    for location in query:
        if len(location.data) == 0:
            continue
        last_log = model_to_dict(location.data[0])
        previous_log = (
            model_to_dict(location.data[1])
            if len(location.data) > 1
            else dict(infected=0, cured=0, deaths=0)
        )
        results.append(
            dict(
                location=location.location,
                last_updated=location.last_updated,
                infected=last_log["infected"],
                cured=last_log["cured"],
                deaths=last_log["deaths"],
                infected_delta=last_log["infected"] - previous_log["infected"],
                cured_delta=last_log["cured"] - previous_log["cured"],
                deaths_delta=last_log["deaths"] - previous_log["deaths"],
                infected_females=last_log["infected_females"],
                infected_males=last_log["infected"] - last_log["infected_females"],
            )
        )
    return results
