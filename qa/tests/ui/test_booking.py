from qa.flows.book_cottage_flow import BookCottageFlow
import pytest
from qa.utils.logging_utils import get_logger
logger = get_logger(__name__)
from playwright.sync_api import expect

@pytest.mark.booking
def test_user_can_book(page_instance):
    book_cottage_flow = BookCottageFlow(page_instance)
    with page_instance.expect_event("dialog") as dialog_info:
        book_cottage_flow.complete_booking(
            'Chris Melski',
            'c_melski@yahoo.com',
            '2026-05-26',
            '2026-05-28',
            '4',
            'non-smoking'
        )

    dialog = dialog_info.value

    assert dialog.message == "Reservation submitted! Hook this to your backend API."
    logger.info(f'{dialog.message} successfully displayed')

