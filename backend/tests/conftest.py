import os

import pytest
from coronastats import create_app, db_wrapper
from coronastats.migrations import migrate, migrations


@pytest.fixture(scope="session")
def app():
    os.environ["CORONASTATS_CONFIG"] = "coronastats.config.TestConfig"
    os.environ["CORONASTATS_SECRET_KEY"] = "test"
    app = create_app()
    with app.app_context():
        yield app


@pytest.fixture(scope="session")
def setup_db(app):
    migrate(len(migrations))
    yield
    os.remove(app.config["DATABASE_PATH"])


@pytest.fixture()
def db(setup_db):
    database = db_wrapper.database
    with database.atomic() as transaction:
        yield
        transaction.rollback()
