import pytest
from qa.tests.fixtures.reservation_fixtures import create_single_booking
from qa.business_logic.api.reservation_api import ReservationAPI
from qa.core.utils.common_utils import convert_booking_details_tuple_to_dictionary
from datetime import timedelta, datetime

@pytest.mark.check_availability_api_no_availability
def test_check_availability_api_no_availability(reset_db, api_client, create_single_booking):
    reservation_api = ReservationAPI(api_client)
    new_booking_dict = convert_booking_details_tuple_to_dictionary(create_single_booking)
    response = reservation_api.add_reservation(new_booking_dict)
    assert response.status_code == 201
    checkin = create_single_booking[2]
    checkout = create_single_booking[3]
    params = {
        'checkin': checkin,
        'checkout': checkout
    }
    response = reservation_api.check_availability(params=params)
    assert response.status_code == 200
    availability_results = response.json()
    print(availability_results)
    for result in availability_results:
        assert result['available'] is False

@pytest.mark.check_availability_api_available
def test_check_availability_api_no_available(reset_db, api_client, create_single_booking):
    reservation_api = ReservationAPI(api_client)
    new_booking_dict = convert_booking_details_tuple_to_dictionary(create_single_booking)
    response = reservation_api.add_reservation(new_booking_dict)
    assert response.status_code == 201
    # use the checkout date as the checkin date and convert to datetime object
    checkin = datetime.strptime(
        create_single_booking[3],
        "%Y-%m-%d"
    ).date()
    checkout = checkin + timedelta(days=3)
    params = {
        'checkin': checkin,
        'checkout': checkout
    }
    response = reservation_api.check_availability(params=params)
    assert response.status_code == 200
    availability_results = response.json()
    print(availability_results)
    for result in availability_results:
        assert result['available'] is True
