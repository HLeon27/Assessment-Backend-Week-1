"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime, date

from flask import Flask, Response, request, jsonify

from date_functions import (convert_to_datetime, get_day_of_week_on,
                            get_days_between, get_current_age)

app_history = []

app = Flask(__name__)


def add_to_history(current_request):
    """Adds a route to the app history."""
    app_history.append({
        "method": current_request.method,
        "at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "route": current_request.endpoint
    })


def clear_history():
    """Clears the app history."""
    app_history.clear()


@app.get("/")
def index():
    """Returns an API welcome messsage."""
    return jsonify({"message": "Welcome to the Days API."})


@app.post("/between")
def get_days_between_dates():
    if request.method != "POST":
        return 405
    data = request.get_json()
    if "first" not in data or "last" not in data:
        return {"error": "Missing required data."}, 400
    if not isinstance(data["first"], str) or not isinstance(data["last"], str):
        return {"error": "Unable to convert value to datetime."}, 400
    if len(data["first"].split(".")) == 1 or len(data["last"].split(".")) == 0:
        return {"error": "Unable to convert value to datetime."}, 400

    first = convert_to_datetime(data["first"])
    last = convert_to_datetime(data["last"])
    days_diff = get_days_between(first, last)
    add_to_history(request)
    return {"days": days_diff}, 200


@app.post("/weekday")
def get_weekday():
    if request.method != "POST":
        return 405
    data = request.get_json()
    request_date = data.get("date")
    if not request_date:
        return {"error": "Missing required data."}, 400
    if not isinstance(request_date, str):
        return {"error": "Unable to convert value to datetime."}, 400
    split_date = request_date.split(".")
    if len(split_date) == 1 or len(split_date[-1]) < 4:
        return {"error": "Unable to convert value to datetime."}, 400

    request_datetime = convert_to_datetime(request_date)
    weekday = get_day_of_week_on(request_datetime)
    add_to_history(request)
    return {"weekday": weekday}, 200


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(port=8080, debug=True)
