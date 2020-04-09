from flask import current_app

from coronastats import db, cache

app = current_app


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


@app.route("/api/get_last_log_by_location/", methods=["GET"])
@cache.cached(timeout=3600)
def get_last_log_by_location():
    results = db.get_last_log_by_location()
    return {"results": results}
