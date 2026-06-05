from qa.business_logic.pages.landing_page import LandingPage
from qa.business_logic.pages.confirmation_page import ConfirmationPage
from qa.core.utils.logging_utils import get_logger
logger = get_logger(__name__)


class BookCottageFlow:

    def __init__(self, page):
        self.page = page

    def complete_booking(self, full_name, email, checkin, checkout, guest_count, requests):
        landing_page = LandingPage(self.page)
        landing_page.enter_full_name(full_name)
        name_input = landing_page.full_name.input_value()
        logger.info(f'name: {name_input}')
        landing_page.enter_email(email)
        email_input = landing_page.email.input_value()
        logger.info(f'email: {email_input}')
        landing_page.select_checkin_date(checkin)
        checkin_input = landing_page.checkin_date.input_value()
        logger.info(f'checkin: {checkin_input}')
        landing_page.select_checkout_date(checkout)
        checkout_input = landing_page.checkout_date.input_value()
        logger.info(f'checkout: {checkout_input}')
        landing_page.select_number_of_guests(guest_count)
        guests_input = landing_page.number_of_guests.input_value()
        logger.info(f'guests: {guests_input}')
        landing_page.enter_special_requests(requests)
        requests_input = landing_page.special_requests.input_value()
        logger.info(f'requests: {requests_input}')
        cottage_nickname = landing_page.cottage_nickname_input.input_value()
        logger.info(f'Cottage nickname: {cottage_nickname}')

        self.page.evaluate("""
        () => {
          document.getElementById('checkin').dispatchEvent(new Event('change'));
          document.getElementById('checkout').dispatchEvent(new Event('change'));
        }
        """)
        # self.page.wait_for_function(
        #       "Number(document.getElementById('total_price_input').value) > 0"
        #   )
        # self.page.wait_for_function(
        #     "document.getElementById('total_price_input').value !== ''"
        # )
        self.page.wait_for_function(
            "document.getElementById('price').textContent.includes('$')"
        )
        #expect(landing_page.booking_form.total_price_input).not_to_have_value("")
        logger.info('About to submit')
        price = landing_page.total_price_input.input_value()
        logger.info(f'Price: {price}')
        landing_page.click_reserve()
        logger.info('Submit hit')
        return ConfirmationPage(self.page)

