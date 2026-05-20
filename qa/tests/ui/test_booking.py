from qa.flows.book_cottage_flow import BookCottageFlow
import pytest
from qa.utils.logging_utils import get_logger
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

@pytest.mark.booking
def test_user_can_book(page_instance, new_booking_data):
    book_cottage_flow = BookCottageFlow(page_instance)

    confirmation = book_cottage_flow.complete_booking(
        new_booking_data['full_name'],
        new_booking_data['email'],
        new_booking_data['checkin_date'],
        new_booking_data['checkout_date'],
        new_booking_data['number_of_guests'],
        new_booking_data['special_requests']
        )

    expect(confirmation.heading_one).to_be_visible()
    expect(confirmation.heading_one).to_contain_text('Booking confirmed')
    logger.info(f'{confirmation.heading_one.inner_text()} text successfully displayed')

