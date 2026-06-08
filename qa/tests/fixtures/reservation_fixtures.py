import pytest
from qa.business_logic.data.new_booking import NewBooking

MULTIPLE_BOOKING_COUNT = 10


@pytest.fixture()
def create_single_booking():
    new_booking = NewBooking()
    return new_booking.generate_new_reservation_details()


@pytest.fixture()
def create_multiple_bookings():
    new_booking = NewBooking()
    return [new_booking.generate_new_reservation_details() for i in range(MULTIPLE_BOOKING_COUNT)]
