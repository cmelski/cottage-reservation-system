from qa.core.ui.ui_actions import UIActions
class ConfirmationPage:

    def __init__(self, page):
        self.page = page
        self.ui_actions = UIActions(self.page)
        self.heading_one = page.locator('h1')
        self.confirmation_message = page.locator('p')
        self.return_home_button = page.get_by_test_id("return-home")

    def click_return_home(self):
        self.ui_actions.click_element(self.return_home_button)