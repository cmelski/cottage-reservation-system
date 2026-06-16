from qa.business_logic.api.reservation_api import ReservationAPI
from qa.business_logic.facades.reservation_facade import ReservationFacade
from qa.business_logic.flows.book_cottage_flow import BookCottageFlow
from qa.tests.fixtures.reservation_fixtures import create_single_booking, create_multiple_bookings
import pytest
from qa.core.utils.logging_utils import get_logger

logger = get_logger(__name__)
from playwright.sync_api import expect


# @pytest.mark.booking_jscript_dialog
# def test_user_can_book_(page_instance):
#     book_cottage_flow = BookCottageFlow(page_instance)
#     with page_instance.expect_event("dialog") as dialog_info:
#         book_cottage_flow.complete_booking(
#             'Chris Melski',
#             'cdffdf@yahoo.com',
#             '2026-05-26',
#             '2026-05-28',
#             '4',
#             'non-smoking'
#         )
#
#     dialog = dialog_info.value
#
#     assert dialog.message == "Reservation submitted! Hook this to your backend API."
#     logger.info(f'{dialog.message} successfully displayed')
@pytest.mark.smoke
@pytest.mark.single_booking
def test_single_booking(reset_db, page_instance, api_client, create_single_booking):
    reservation_facade = ReservationFacade(page_instance, api_client, create_single_booking)
    reservation = reservation_facade.create_reservation()

    assert 'Booking confirmed' in reservation[0]['heading_one_text']
    assert isinstance(reservation[0]['booking_id'], int)
    logger.info(f'{reservation[0]["heading_one_text"]}')
    logger.info(f'{reservation[0]["confirmation_text"]}')
    logger.info(f'Booking ID: {reservation[0]["booking_id"]}')

    new_booking_data = list(create_single_booking)
    assert reservation[1] == new_booking_data
    logger.info(f'API response data: {reservation[1]} matches new booking data: '
                 f'{new_booking_data}')

@pytest.mark.multiple_bookings
def test_multiple_bookings(reset_db, page_instance, create_multiple_bookings, api_client):
    book_cottage_flow = BookCottageFlow(page_instance)
    reservation_api = ReservationAPI(api_client)

    for booking in create_multiple_bookings:
        confirmation = book_cottage_flow.complete_booking(booking)
        booking_details = confirmation.get_confirmation_details()

        expect(confirmation.heading_one).to_be_visible()
        expect(confirmation.heading_one).to_contain_text('Booking confirmed', timeout=10000)
        logger.info(f'{confirmation.heading_one.inner_text()} text successfully displayed')
        logger.info(f'{confirmation.confirmation_message.inner_text()}')

        booking_id_confirmation_page = booking_details['booking_id']
        booking_api_response = reservation_api.get_reservation(booking_id_confirmation_page)
        response_status = booking_api_response.status_code
        assert response_status == 200
        booking_api_data = booking_api_response.json()['booking']
        booking_id_api = booking_api_data['booking_id']
        assert booking_id_api == booking_id_confirmation_page
        logger.info(f'UI booking id: {booking_id_confirmation_page} matches booking id from api call: '
                    f'{booking_id_api}')

        api_response_data = [
            booking_api_data["full_name"],
            booking_api_data["email"],
            booking_api_data["checkin_date"],
            booking_api_data["checkout_date"],
            booking_api_data["number_of_guests"],
            booking_api_data["special_requests"],
            float(booking_api_data["total_price"]),
            booking_api_data["status"]
        ]
        new_booking_data = list(booking)

        assert api_response_data == new_booking_data

        logger.info(f'API response data: {api_response_data} matches new booking data: '
                    f'{new_booking_data}')

        confirmation.click_return_home()
