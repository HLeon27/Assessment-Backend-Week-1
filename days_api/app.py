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


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(port=8080, debug=True)
