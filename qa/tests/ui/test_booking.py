import os

from qa.business_logic.flows.book_cottage_flow import BookCottageFlow
from qa.business_logic.api.reservation_api import ReservationAPI
from qa.core.api.api_client import APIClient
import pytest
from qa.core.utils.logging_utils import get_logger
from qa.tests.fixtures.reservation_fixtures import create_single_booking, create_multiple_bookings

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

@pytest.mark.single_booking
def test_single_booking(reset_db, page_instance, create_single_booking):
    book_cottage_flow = BookCottageFlow(page_instance)

    confirmation = book_cottage_flow.complete_booking(create_single_booking)

    expect(confirmation.heading_one).to_be_visible()
    expect(confirmation.heading_one).to_contain_text('Booking confirmed', timeout=10000)
    logger.info(f'{confirmation.heading_one.inner_text()} text successfully displayed')
    logger.info(f'{confirmation.confirmation_message.inner_text()}')

    # get booking id on the confirmation page

    booking_id_confirmation_page = confirmation.get_booking_id()

    # get the booking via api call

    api_client = APIClient(os.environ.get('BASE_URL'))
    reservation_api = ReservationAPI(api_client)
    booking_api_response = reservation_api.get_reservation(booking_id_confirmation_page)
    response_status = booking_api_response.status_code
    assert response_status == 200
    booking_api_data = booking_api_response.json()['booking']
    booking_id_api = booking_api_data['booking_id']
    assert booking_id_api == booking_id_confirmation_page
    logger.info(f'UI booking id: {booking_id_confirmation_page} matches booking id from api call: '
                f'{booking_api_data['booking_id']}')


@pytest.mark.multiple_bookings
def test_multiple_bookings(reset_db, page_instance, create_multiple_bookings):
    book_cottage_flow = BookCottageFlow(page_instance)
    api_client = APIClient(os.environ.get('BASE_URL'))
    reservation_api = ReservationAPI(api_client)

    for booking in create_multiple_bookings:
        confirmation = book_cottage_flow.complete_booking(booking)

        expect(confirmation.heading_one).to_be_visible()
        expect(confirmation.heading_one).to_contain_text('Booking confirmed', timeout=10000)
        logger.info(f'{confirmation.heading_one.inner_text()} text successfully displayed')
        logger.info(f'{confirmation.confirmation_message.inner_text()}')

        booking_id_confirmation_page = confirmation.get_booking_id()
        booking_api_response = reservation_api.get_reservation(booking_id_confirmation_page)
        response_status = booking_api_response.status_code
        assert response_status == 200
        booking_api_data = booking_api_response.json()['booking']
        booking_id_api = booking_api_data['booking_id']
        assert booking_id_api == booking_id_confirmation_page
        logger.info(f'UI booking id: {booking_id_confirmation_page} matches booking id from api call: '
                    f'{booking_api_data['booking_id']}')

        confirmation.click_return_home()
