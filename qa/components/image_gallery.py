
class ImageGallery:

    def __init__(self, page):
        self.page = page
        self.gallery = page.get_by_test_id("image-gallery")

    def scroll_left(self):
        gallery = self.gallery
        gallery.hover()
        self.page.mouse.wheel(500, 0)
        scroll_pos = gallery.evaluate("el => el.scrollLeft")
        return scroll_pos

    def scroll_right(self):
        gallery = self.gallery
        gallery.hover()
        self.page.mouse.wheel(-500, 0)
        scroll_pos = gallery.evaluate("el => el.scrollLeft")
        return scroll_pos
