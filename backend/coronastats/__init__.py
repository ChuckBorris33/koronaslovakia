import os

from flask import Flask
from flask_cors import CORS
from flask_caching import Cache

cache = Cache()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    CORS(app, resources={r"*": {"origins": "*"}})
    config_path = os.getenv('CORONASTATS_CONFIG', 'coronastats.config.ProductionConfig')
    app.config.from_object(config_path)

    cache.init_app(app)

    with app.app_context():
        from . import routes
        from . import commands
        return app
