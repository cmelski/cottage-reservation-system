class BookingForm:

    def __init__(self, page):
        self.page = page
        self.full_name = page.get_by_test_id("full-name")
        self.email = page.get_by_test_id("email")
        self.checkin_date = page.get_by_test_id("checkin-date")
        self.checkout_date = page.get_by_test_id("checkout-date")
        self.number_of_guests = page.get_by_test_id("number-of-guests")
        self.special_requests = page.get_by_test_id("special-requests")
        self.reserve_button = page.get_by_test_id("reserve-button")

    def enter_full_name(self, full_name):
        self.full_name.fill(full_name)

    def enter_email(self, email):
        self.email.fill(email)

    def select_checkin_date(self, checkin_date):
        self.checkin_date.fill(checkin_date)

    def select_checkout_date(self, checkout_date):
        self.checkout_date.fill(checkout_date)

    def select_number_of_guests(self, number_of_guests):
        self.number_of_guests.select_option(number_of_guests)

    def enter_special_requests(self, special_requests):
        self.special_requests.fill(special_requests)

    def click_reserve(self):
        self.reserve_button.click()

