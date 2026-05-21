
class ImageGallery:

    def __init__(self, page):
        self.page = page
        self.gallery = page.get_by_test_id("image-gallery")

    def get_image_count(self):
        image_count = self.gallery.locator('img').count()
        return image_count

