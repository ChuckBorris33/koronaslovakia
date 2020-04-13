import logging
import os
import sys
from logging.config import dictConfig

from flask import Flask, current_app
from flask_cors import CORS
from flask_caching import Cache
from peewee import SqliteDatabase
from playhouse.flask_utils import FlaskDB


class LogFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno < logging.WARNING


dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s: %(message)s"
            }
        },
        "filters": {
            "log": {
                "()": LogFilter,
            }
        },
        "handlers": {
            "log": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "default",
                "filters": ["log"]
            },
            "error": {
                "class": "logging.StreamHandler",
                "stream": sys.stderr,
                "formatter": "default",
                'level': 'WARN',
            },
        },
        "root": {"level": os.getenv('CORONASTATS_LOGLEVEL', "INFO"), "handlers": ["log", "error"]},
    }
)

cache = Cache()
db_wrapper = FlaskDB()


def create_app():
    app = Flask("coronastats", instance_relative_config=False)
    CORS(app, resources={r"*": {"origins": "*"}})
    config_path = os.getenv("CORONASTATS_CONFIG", "coronastats.config.ProductionConfig")
    app.config.from_object(config_path)

    db_wrapper.init_app(app)
    cache.init_app(app)

    with app.app_context():
        from . import routes
        from . import commands

        return app
