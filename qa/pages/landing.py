from qa.components.image_gallery import ImageGallery


class LandingPage:
    HEADING_ONE = 'Cabot Trail Serenity Stay'

    def __init__(self, page):
        self.page = page
        self.image_gallery = ImageGallery(page)
        self.heading_one = page.locator('h1')

