from qa.core.ui.ui_actions import UIActions
class LandingPage:
    HEADING_ONE = 'Cabot Trail Serenity Stay'

    def __init__(self, page):
        self.page = page
        self.ui_actions = UIActions(page)
        self.gallery = page.get_by_test_id("image-gallery")
        self.heading_one = page.locator('h1')
        self.full_name = page.get_by_test_id("full-name")
        self.email = page.get_by_test_id("email")
        self.checkin_date = page.get_by_test_id("checkin-date")
        self.checkout_date = page.get_by_test_id("checkout-date")
        self.number_of_guests = page.get_by_test_id("number-of-guests")
        self.special_requests = page.get_by_test_id("special-requests")
        self.total_price = page.locator("#price")
        self.total_price_input = page.locator("#total_price_input")
        self.cottage_nickname_input = page.locator("#cottage_nickname_input")
        self.reserve_button = page.get_by_test_id("reserve-button")

    def enter_full_name(self, full_name):
        self.ui_actions.enter_text(self.full_name, full_name)

    def enter_email(self, email):
        self.ui_actions.enter_text(self.email, email)

    def select_checkin_date(self, checkin_date):
        self.ui_actions.enter_text(self.checkin_date, checkin_date)

    def select_checkout_date(self, checkout_date):
        self.ui_actions.enter_text(self.checkout_date, checkout_date)

    def select_number_of_guests(self, number_of_guests):
        self.ui_actions.select_option(self.number_of_guests, number_of_guests)

    def enter_special_requests(self, special_requests):
        self.ui_actions.enter_text(self.special_requests, special_requests)

    def click_reserve(self):
        self.ui_actions.click_element(self.reserve_button)

    def get_image_count(self):
        return self.ui_actions.get_element_count(self.gallery, 'img')



