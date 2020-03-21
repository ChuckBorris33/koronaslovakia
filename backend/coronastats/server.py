import os

from flask import Flask
from flask_cors import CORS

from coronastats import db


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", default=None)
    CORS(app, resources={r"*": {"origins": "*"}})

    @app.route("/api/infected_log/", methods=["GET"])
    def infected_log():
        results = db.get_infected_log()
        return {"results": list(results)}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
