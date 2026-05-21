
class ConfirmationPage:

    def __init__(self, page):
        self.page = page
        self.heading_one = page.locator('h1')
        self.confirmation_message = page.locator('p')