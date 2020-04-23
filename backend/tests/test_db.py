import datetime

import pytest
from coronastats import db
from playhouse.shortcuts import model_to_dict

pytestmark = pytest.mark.usefixtures("db")


def test_add_corona_log_inserts_new():
    assert list(db.CoronaLog.select()) == []

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    db.add_corona_log(infected=1, tests=2, deaths=3, cured=4)
    db.add_corona_log(log_date=yesterday, infected=11, tests=22, deaths=33, cured=44)

    assert list(db.CoronaLog.select().dicts()) == [
        dict(id=1, date=today, infected=1, cured=4, tests=2, deaths=3),
        dict(id=2, date=yesterday, infected=11, cured=44, tests=22, deaths=33),
    ]


def test_add_corona_log_update():
    db.add_corona_log(infected=1, tests=2, deaths=3, cured=4)
    db.add_corona_log(infected=10, tests=20, deaths=30, cured=40)

    assert list(db.CoronaLog.select().dicts()) == [
        dict(
            id=1, date=datetime.date.today(), infected=10, cured=40, tests=20, deaths=30
        )
    ]


def test_get_log_by_date_existing():
    today = datetime.date.today()
    today_log_id = db.CoronaLog.create(
        date=today, infected=1, tests=2, deaths=3, cured=4
    )
    today_log = db.CoronaLog.get_by_id(today_log_id)
    log, created = db.get_log_by_date(today)
    assert not created
    assert log == today_log


def test_get_log_by_date_new():
    today = datetime.date.today()
    log, created = db.get_log_by_date(today)
    assert created
    assert model_to_dict(log) == dict(
        id=1, date=today, infected=0, cured=0, tests=0, deaths=0
    )


def test_get_last_log_date():
    today = datetime.date.today()
    db.CoronaLog.create(date=today - datetime.timedelta(days=30))
    db.CoronaLog.create(date=today - datetime.timedelta(days=17))
    db.CoronaLog.create(date=today - datetime.timedelta(days=15))
    assert db.get_last_log_date() == today - datetime.timedelta(days=15)
    db.CoronaLog.create(date=today)
    assert db.get_last_log_date() == today


def test_get_infected_log():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    db.CoronaLog.create(date=yesterday, infected=1, tests=2, deaths=3, cured=4)
    db.CoronaLog.create(infected=11, tests=22, deaths=33, cured=44)

    assert list(db.get_infected_log()) == [
        dict(date=yesterday, infected=1, cured=4, tests=2, deaths=3),
        dict(date=today, infected=11, cured=44, tests=22, deaths=33),
    ]


def test_get_infected_increase_log():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    day_before_yesterday = today - datetime.timedelta(days=2)
    db.CoronaLog.create(
        date=day_before_yesterday, infected=1, tests=2, deaths=3, cured=4
    )
    db.CoronaLog.create(date=yesterday, infected=11, tests=12, deaths=13, cured=14)
    db.CoronaLog.create(date=today, infected=31, tests=32, deaths=33, cured=34)

    assert list(db.get_infected_increase_log()) == [
        dict(
            date=day_before_yesterday,
            infected_increase=1,
            cured_increase=4,
            tests_increase=2,
            deaths_increase=3,
        ),
        dict(
            date=yesterday,
            infected_increase=10,
            cured_increase=10,
            tests_increase=10,
            deaths_increase=10,
        ),
        dict(
            date=today,
            infected_increase=20,
            cured_increase=20,
            tests_increase=20,
            deaths_increase=20,
        ),
    ]


def test_get_last_log_by_location_first_logs():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    location_1 = db.CoronaLocation.create(location="Horna")
    location_2 = db.CoronaLocation.create(location="Dolna", last_updated=yesterday)
    db.CoronaLocation.create(location="NoData")
    db.CoronaLocationLog.create(
        location=location_1, infected=5, infected_females=1, tests=2, deaths=3, cured=4
    )
    db.CoronaLocationLog.create(
        location=location_2, infected=10, infected_females=5, tests=3, deaths=4, cured=5
    )
    assert db.get_last_log_by_location() == [
        dict(
            location=location_1.location,
            last_updated=location_1.last_updated,
            infected=5,
            cured=4,
            deaths=3,
            infected_delta=5,
            cured_delta=4,
            deaths_delta=3,
            infected_females=1,
            infected_males=4,
        ),
        dict(
            location=location_2.location,
            last_updated=location_2.last_updated,
            infected=10,
            cured=5,
            deaths=4,
            infected_delta=10,
            cured_delta=5,
            deaths_delta=4,
            infected_females=5,
            infected_males=5,
        ),
    ]


@pytest.mark.parametrize("first_timedelta, second_timedelta", [(1, 0), (2, 1)])
def test_get_last_log_by_location_with_delta(first_timedelta, second_timedelta):
    date1 = datetime.date.today() - datetime.timedelta(days=first_timedelta)
    date2 = datetime.date.today() - datetime.timedelta(days=second_timedelta)
    location_1 = db.CoronaLocation.create(location="Horna", last_updated=date1)
    location_2 = db.CoronaLocation.create(location="Dolna", last_updated=date2)
    db.CoronaLocationLog.create(
        date=date1,
        location=location_1,
        infected=5,
        infected_females=1,
        tests=2,
        deaths=3,
        cured=4,
    )
    db.CoronaLocationLog.create(
        date=date1,
        location=location_2,
        infected=10,
        infected_females=5,
        tests=3,
        deaths=4,
        cured=5,
    )
    db.CoronaLocationLog.create(
        date=date2,
        location=location_1,
        infected=6,
        infected_females=2,
        tests=3,
        deaths=4,
        cured=5,
    )
    db.CoronaLocationLog.create(
        date=date2,
        location=location_2,
        infected=12,
        infected_females=7,
        tests=5,
        deaths=6,
        cured=7,
    )
    assert db.get_last_log_by_location() == [
        dict(
            location=location_1.location,
            last_updated=location_1.last_updated,
            infected=6,
            cured=5,
            deaths=4,
            infected_delta=1,
            cured_delta=1,
            deaths_delta=1,
            infected_females=2,
            infected_males=4,
        ),
        dict(
            location=location_2.location,
            last_updated=location_2.last_updated,
            infected=12,
            cured=7,
            deaths=6,
            infected_delta=2,
            cured_delta=2,
            deaths_delta=2,
            infected_females=7,
            infected_males=5,
        ),
    ]
