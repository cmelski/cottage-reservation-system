class UIActions:

    def __init__(self, page):
        self.page = page

    def enter_text(self, element, text):
        element.fill(text)

    def select_option(self, element, option):
        element.select_option(option)

    def click_element(self, element):
        element.click()

    def get_element_count(self, element, selector=None):
        if selector:
            element_count = element.locator(selector).count()
        else:
            element_count = element.count()
        return element_count
