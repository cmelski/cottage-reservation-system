from qa.pages.landing_page import LandingPage


class BookCottageFlow:

    def __init__(self, page):
        self.page = page

    def complete_booking(self, full_name, email, checkin, checkout, guest_count, requests):
        landing_page = LandingPage(self.page)
        landing_page.booking_form.enter_full_name(full_name)
        landing_page.booking_form.enter_email(email)
        landing_page.booking_form.select_checkin_date(checkin)
        landing_page.booking_form.select_checkout_date(checkout)
        landing_page.booking_form.select_number_of_guests(guest_count)
        landing_page.booking_form.enter_special_requests(requests)
        landing_page.booking_form.click_reserve()
