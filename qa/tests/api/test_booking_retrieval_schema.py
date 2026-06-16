import pytest
from qa.tests.fixtures.reservation_fixtures import create_single_booking
from qa.business_logic.api.reservation_api import BookingResponse, ReservationAPI
from qa.business_logic.db_queries.db_queries import add_booking_to_db

@pytest.mark.smoke
def test_booking_schema(reset_db, api_client, db_client, create_single_booking):
    # add a new booking directly through DB call

    new_booking = add_booking_to_db(create_single_booking, db_client)
    booking_id = new_booking[1]

    reservation_api = ReservationAPI(api_client)

    response = reservation_api.get_reservation(booking_id)

    BookingResponse(**response.json()['booking'])
