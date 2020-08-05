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
from playhouse.shortcuts import model_to_dict, update_model_from_dict


class CoronaLog(db_wrapper.Model):  # type: ignore
    id = AutoField()
    date = DateField(default=datetime.date.today(), unique=True, index=True)
    infected = IntegerField(default=0)
    cured = IntegerField(default=0)
    tests = IntegerField(default=0)
    deaths = IntegerField(default=0)
    median = IntegerField(default=0)
    hospitalized = IntegerField(default=0)
    confirmed_hospitalized = IntegerField(default=0)
    confirmed_hospitalized_icu = IntegerField(default=0)
    confirmed_hospitalized_ventilation = IntegerField(default=0)


class CoronaLocation(db_wrapper.Model):  # type: ignore
    id = AutoField()
    location = CharField(index=True)
    last_updated = DateField(default=datetime.date.today())


class CoronaLocationLog(db_wrapper.Model):  # type: ignore
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
    log_date: typing.Optional[datetime.date] = None,
    median: int = 0,
    hospitalized: int = 0,
    confirmed_hospitalized: int = 0,
    confirmed_hospitalized_icu: int = 0,
    confirmed_hospitalized_ventilation: int = 0,
) -> int:
    if not log_date:
        log_date = datetime.date.today()
    values = dict(
        infected=infected,
        cured=cured,
        tests=tests,
        deaths=deaths,
        median=median,
        hospitalized=hospitalized,
        confirmed_hospitalized=confirmed_hospitalized,
        confirmed_hospitalized_icu=confirmed_hospitalized_icu,
        confirmed_hospitalized_ventilation=confirmed_hospitalized_ventilation,
    )
    log, created = CoronaLog.get_or_create(date=log_date, defaults=values)
    if not created:
        update_model_from_dict(log, values)
        log.save()
    return log.id


def get_log_by_date(log_date):
    return CoronaLog.get_or_create(date=log_date)


def get_last_log_date() -> datetime.date:
    return CoronaLog.select(CoronaLog.date).order_by(CoronaLog.date.desc()).get().date


def get_infected_log() -> typing.Iterable[dict]:
    return CoronaLog.select(
        CoronaLog.date,
        CoronaLog.infected,
        CoronaLog.cured,
        CoronaLog.tests,
        CoronaLog.deaths,
        CoronaLog.median,
        CoronaLog.hospitalized,
        CoronaLog.confirmed_hospitalized,
        CoronaLog.confirmed_hospitalized_icu,
        CoronaLog.confirmed_hospitalized_ventilation,
    ).dicts()


def get_infected_increase_log() -> typing.Iterable[dict]:
    CoronaLogPrevieous = CoronaLog.alias()
    previous_query = CoronaLogPrevieous.select()
    previous_query = previous_query.alias("clp")

    return (
        CoronaLog.select(
            CoronaLog.date,
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
            Value(CoronaLog.median - fn.COALESCE(previous_query.c.median, 0)).alias(
                "median_increase"
            ),
            Value(
                CoronaLog.hospitalized - fn.COALESCE(previous_query.c.hospitalized, 0)
            ).alias("hospitalized_increase"),
            Value(
                CoronaLog.confirmed_hospitalized
                - fn.COALESCE(previous_query.c.confirmed_hospitalized, 0)
            ).alias("confirmed_hospitalized_increase"),
            Value(
                CoronaLog.confirmed_hospitalized_icu
                - fn.COALESCE(previous_query.c.confirmed_hospitalized_icu, 0)
            ).alias("confirmed_hospitalized_icu_increase"),
            Value(
                CoronaLog.confirmed_hospitalized_ventilation
                - fn.COALESCE(previous_query.c.confirmed_hospitalized_ventilation, 0)
            ).alias("confirmed_hospitalized_ventilation"),
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
                infected_delta=last_log["infected"] - previous_log["infected"],
            )
        )
    return results
