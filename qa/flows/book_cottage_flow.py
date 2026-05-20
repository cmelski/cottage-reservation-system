from qa.pages.landing_page import LandingPage
from qa.pages.confirmation_page import ConfirmationPage
from playwright.sync_api import expect
from qa.utils.logging_utils import get_logger
logger = get_logger(__name__)


class BookCottageFlow:

    def __init__(self, page):
        self.page = page

    def complete_booking(self, full_name, email, checkin, checkout, guest_count, requests):
        landing_page = LandingPage(self.page)
        landing_page.booking_form.enter_full_name(full_name)
        name_input = landing_page.booking_form.full_name.input_value()
        logger.info(f'name: {name_input}')
        landing_page.booking_form.enter_email(email)
        email_input = landing_page.booking_form.email.input_value()
        logger.info(f'email: {email_input}')
        landing_page.booking_form.select_checkin_date(checkin)
        checkin_input = landing_page.booking_form.checkin_date.input_value()
        logger.info(f'checkin: {checkin_input}')
        landing_page.booking_form.select_checkout_date(checkout)
        checkout_input = landing_page.booking_form.checkout_date.input_value()
        logger.info(f'checkout: {checkout_input}')
        landing_page.booking_form.select_number_of_guests(guest_count)
        guests_input = landing_page.booking_form.number_of_guests.input_value()
        logger.info(f'guests: {guests_input}')
        landing_page.booking_form.enter_special_requests(requests)
        requests_input = landing_page.booking_form.special_requests.input_value()
        logger.info(f'requests: {requests_input}')
        # self.page.wait_for_function(
        #      "Number(document.getElementById('total_price_input').value) > 0"
        #  )
        #expect(landing_page.booking_form.total_price_input).not_to_have_value("")
        landing_page.booking_form.click_reserve()
        #return ConfirmationPage(self.page)

