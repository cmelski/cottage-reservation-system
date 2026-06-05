from qa.business_logic.flows.book_cottage_flow import BookCottageFlow
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

@pytest.mark.single_booking
def test_user_can_book(reset_db, page_instance, create_single_booking):
    book_cottage_flow = BookCottageFlow(page_instance)

    confirmation = book_cottage_flow.complete_booking(
        create_single_booking[0],
        create_single_booking[1],
        create_single_booking[2],
        create_single_booking[3],
        create_single_booking[4],
        create_single_booking[5]
    )

    expect(confirmation.heading_one).to_be_visible()
    expect(confirmation.heading_one).to_contain_text('Booking confirmed', timeout=10000)
    logger.info(f'{confirmation.heading_one.inner_text()} text successfully displayed')
    logger.info(f'{confirmation.confirmation_message.inner_text()}')

@pytest.mark.multiple_bookings
def test_multiple_bookings(reset_db, page_instance, create_multiple_bookings):
    book_cottage_flow = BookCottageFlow(page_instance)

    for booking in create_multiple_bookings:

        confirmation = book_cottage_flow.complete_booking(
            booking[0],
            booking[1],
            booking[2],
            booking[3],
            booking[4],
            booking[5]
        )

        expect(confirmation.heading_one).to_be_visible()
        expect(confirmation.heading_one).to_contain_text('Booking confirmed', timeout=10000)
        logger.info(f'{confirmation.heading_one.inner_text()} text successfully displayed')
        logger.info(f'{confirmation.confirmation_message.inner_text()}')

        confirmation.click_return_home()

