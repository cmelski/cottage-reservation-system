from qa.core.ui.ui_actions import UIActions


class ConfirmationPage:

    def __init__(self, page):
        self.page = page
        self.ui_actions = UIActions(self.page)
        self.heading_one = page.locator('h1')
        self.confirmation_message = page.locator('p')
        self.return_home_button = page.get_by_test_id("return-home")
        self.booking_id = page.get_by_test_id("booking-id")

    def click_return_home(self):
        self.ui_actions.click_element(self.return_home_button)

    def get_confirmation_details(self):
        booking_id = int(self.booking_id.inner_text().split('#')[1])
        heading_one_text = self.heading_one.inner_text()
        confirmation_text = self.confirmation_message.inner_text()

        return {
            'booking_id': booking_id,
            'heading_one_text': heading_one_text,
            'confirmation_text': confirmation_text
        }
