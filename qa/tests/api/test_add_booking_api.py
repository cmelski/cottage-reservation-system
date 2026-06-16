import pytest
from qa.tests.fixtures.reservation_fixtures import create_single_booking
from qa.business_logic.api.reservation_api import ReservationAPI
from qa.core.utils.common_utils import convert_booking_details_tuple_to_dictionary

@pytest.mark.smoke
@pytest.mark.api_add_booking
def test_add_booking_api(reset_db, api_client, create_single_booking):

    reservation_api = ReservationAPI(api_client)

    new_booking_dict = convert_booking_details_tuple_to_dictionary(create_single_booking)

    response = reservation_api.add_reservation(new_booking_dict)

    assert response.status_code == 201
