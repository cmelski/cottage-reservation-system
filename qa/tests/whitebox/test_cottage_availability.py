from dev.utils.generic_utils import check_availability, get_reservation_dates
from datetime import datetime, date, timedelta
from faker import Faker


def test_check_availability():
    fake = Faker('en_GB')
    checkin = fake.future_date().isoformat()
    checkout = (
            date.fromisoformat(checkin) + timedelta(days=5)
    ).isoformat()
    checkout_date = date.fromisoformat(checkout)

    unavailable_dates = []

    # 5 dates after checkout
    for i in range(1, 6):
        unavailable_dates.append(
            (checkout_date + timedelta(days=i)).isoformat()
        )

    print(f"Check-in:  {checkin}")
    print(f"Check-out: {checkout}")
    print(unavailable_dates)

    assert len(check_availability(checkin, checkout, unavailable_dates)) == 0


def test_check_no_availability():
    fake = Faker('en_GB')
    checkin = fake.future_date().isoformat()
    checkout = (
            date.fromisoformat(checkin) + timedelta(days=5)
    ).isoformat()
    checkin_date = date.fromisoformat(checkin)

    unavailable_dates = []

    # 5 dates between checkin and checkout
    for i in range(0, 5):
        unavailable_dates.append(
            (checkin_date + timedelta(days=i)).isoformat()
        )

    print(f"Check-in:  {checkin}")
    print(f"Check-out: {checkout}")
    print(unavailable_dates)

    assert len(check_availability(checkin, checkout, unavailable_dates)) > 0


def test_get_reserved_dates():
    fake = Faker('en_GB')
    checkin = fake.future_date().isoformat()
    checkout = (
            date.fromisoformat(checkin) + timedelta(days=5)
    ).isoformat()
    print(checkin)
    print(checkout)
    reserved_dates = get_reservation_dates(checkin, checkout)
    print(reserved_dates)
    assert checkin == reserved_dates[0]
    assert reserved_dates[-1] == (
            date.fromisoformat(checkout) - timedelta(days=1)
    ).isoformat()
