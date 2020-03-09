import pytz
import os
from datetime import timedelta, datetime

from dateutil.parser import isoparse
from flask import Flask, request, current_app
from flask_cors import CORS

from poolstats import db


def _get_date_boundary(date_string=None):
    start_datetime = isoparse(date_string) if date_string else datetime.now().date()
    end_datetime = start_datetime + timedelta(1)
    return start_datetime, end_datetime


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", default=None)
    CORS(app, resources={r"*": {"origins": "*"}})

    @app.route("/api/visitor_per_day/", methods=["GET"])
    def visitor_count_per_day():
        date_string = request.args.get("date")
        start_datetime, end_datetime = _get_date_boundary(date_string)
        results = db.get_day_visitor_log(start_datetime, end_datetime)
        serialized_results = []
        for result in results:
            serialized_results.append(
                {
                    "datetime": result.datetime,
                    "visitors": result.visitors,
                }
            )
        return {"results": serialized_results}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
