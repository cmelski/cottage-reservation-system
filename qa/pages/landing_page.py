from qa.components.image_gallery import ImageGallery
from qa.components.booking_form import BookingForm


class LandingPage:
    HEADING_ONE = 'Cabot Trail Serenity Stay'

    def __init__(self, page):
        self.page = page
        self.image_gallery = ImageGallery(page)
        self.booking_form = BookingForm(page)
        self.heading_one = page.locator('h1')

