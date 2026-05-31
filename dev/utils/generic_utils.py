import re
from datetime import datetime, timedelta


def valid_email(email: str) -> bool:
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return bool(re.fullmatch(pattern, email))


def check_availability(checkin: str, checkout: str, existing_dates: list) -> list:
    checkin_date = datetime.strptime(checkin, "%Y-%m-%d").date()
    checkout_date = datetime.strptime(checkout, "%Y-%m-%d").date()

    reserved_dates = []

    current_date = checkin_date
    while current_date < checkout_date:  # checkout date not included
        reserved_dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)

    common_dates = sorted(set(existing_dates) & set(reserved_dates))
    return common_dates


def get_reservation_dates(checkin: str, checkout: str) -> list:
    checkin_date = datetime.strptime(checkin, "%Y-%m-%d").date()
    checkout_date = datetime.strptime(checkout, "%Y-%m-%d").date()

    reserved_dates = []

    current_date = checkin_date
    while current_date < checkout_date:  # checkout date not included
        reserved_dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)

    return reserved_dates
