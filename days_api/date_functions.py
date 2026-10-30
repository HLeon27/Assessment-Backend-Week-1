"""Functions for working with dates."""

from datetime import datetime, date


def convert_to_datetime(date_val: str) -> datetime:
    """Function takes in a string and converts it to a datetime object."""
    try:
        return datetime.strptime(date_val, "%d.%m.%Y")
    except ValueError:
        raise ValueError("Unable to convert value to datetime.")


def get_days_between(first: datetime, last: datetime) -> int:
    if not isinstance(first, datetime) or not isinstance(last, datetime):
        raise TypeError("Datetimes required.")
    time_delta = last - first
    return time_delta.days


def get_day_of_week_on(date_val: datetime) -> str:
    if not isinstance(date_val, datetime):
        raise TypeError("Datetime required.")
    day_of_week_key = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }
    day_of_week = date_val.weekday()
    return day_of_week_key[day_of_week]


def get_current_age(birthdate: date) -> int:
    if not isinstance(birthdate, date):
        raise TypeError("Date required.")

    current_date = date.today()
    years = current_date.year - birthdate.year
    if current_date.month < birthdate.month:
        years -= 1
    elif current_date.month == birthdate.month:
        if current_date.day < birthdate.day:
            years -= 1
    return years


if __name__ == "__main__":
    print(convert_to_datetime("31.02.2013"))
