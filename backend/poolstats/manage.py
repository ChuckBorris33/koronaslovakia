import pytz
from flask_script import Manager

from poolstats import db
from poolstats.server import create_app

manager = Manager(create_app)


@manager.command
def prepare_database():
    db.database.create_tables([db.VisitorLog])


if __name__ == "__main__":
    manager.run()
