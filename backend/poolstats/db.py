import datetime

from peewee import SqliteDatabase, Model, DateTimeField, AutoField, SmallIntegerField

database = SqliteDatabase("../app.db")


class VisitorLog(Model):
    id = AutoField()
    datetime = DateTimeField(default=datetime.datetime.utcnow)
    visitors = SmallIntegerField()

    class Meta:
        database = database


def add_visitor_log(visitor_count):
    VisitorLog.create(visitors=visitor_count)


def get_day_visitor_log(start_datetime, end_datetime):
    return VisitorLog.select().where(
        VisitorLog.datetime.between(start_datetime, end_datetime)
    )

