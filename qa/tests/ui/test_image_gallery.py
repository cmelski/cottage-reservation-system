from qa.pages.landing_page import LandingPage
import pytest
from qa.utils.logging_utils import get_logger
logger = get_logger(__name__)
from playwright.sync_api import expect

@pytest.mark.image_gallery
def test_gallery_scroll(page_instance):
    landing_page = LandingPage(page_instance)
    page_instance.wait_for_function("""
    () => {
      const el = document.querySelector('[data-testid="image-gallery"]');
      return el && el.scrollWidth > el.clientWidth;
    }
    """)
    expect(landing_page.image_gallery.gallery).to_be_visible()
    image_count = page_instance.locator('div[data-testid="image-gallery"] img').count()
    logger.info(f'Image count: {image_count}')
    scroll_pos_left = landing_page.image_gallery.scroll_left()
    assert scroll_pos_left > 0
    logger.info(f'Scroll position left: {scroll_pos_left}')
    scroll_pos_right = landing_page.image_gallery.scroll_right()
    assert scroll_pos_right < scroll_pos_left
    logger.info(f'Scroll position right: {scroll_pos_right}')


