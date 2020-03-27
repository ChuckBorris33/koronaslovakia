import os

from coronastats.cache import cache
from flask import Flask
from flask_cors import CORS

from coronastats import db


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", None)
    cache.init_app(app)
    CORS(app, resources={r"*": {"origins": "*"}})

    @app.route("/api/infected_log/", methods=["GET"])
    @cache.cached(timeout=3600)
    def infected_log():
        results = db.get_infected_log()
        return {"results": list(results)}

    @app.route("/api/infected_increase_log/", methods=["GET"])
    @cache.cached(timeout=3600)
    def infected_increase_log():
        results = db.get_infected_increase_log()
        return {"results": list(results)}

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(debug=True)
