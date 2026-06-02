from dev.utils.generic_utils import get_reservation_dates
from datetime import date, timedelta
from faker import Faker


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
