from qa.pages.landing_page import LandingPage
import pytest
from qa.utils.logging_utils import get_logger
logger = get_logger(__name__)
from playwright.sync_api import expect

@pytest.mark.image_gallery
def test_gallery_scroll(page_instance):
    landing_page = LandingPage(page_instance)
    expect(landing_page.image_gallery.gallery).to_be_visible()
    scroll_pos_left = landing_page.image_gallery.scroll_left()
    assert scroll_pos_left > 0
    logger.info(f'Scroll position left: {scroll_pos_left}')
    scroll_pos_right = landing_page.image_gallery.scroll_right()
    assert scroll_pos_right < scroll_pos_left
    logger.info(f'Scroll position right: {scroll_pos_right}')


