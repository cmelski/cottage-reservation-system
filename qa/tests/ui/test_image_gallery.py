from qa.business_logic.pages.landing_page import LandingPage
import pytest
from qa.core.utils.logging_utils import get_logger

logger = get_logger(__name__)
from playwright.sync_api import expect


@pytest.mark.image_gallery
def test_image_gallery_loading(page_instance):
    landing_page = LandingPage(page_instance)
    expect(landing_page.gallery).to_be_visible()
    gallery_image_count = landing_page.get_image_count()
    logger.info(f'Image count: {gallery_image_count}')
    assert gallery_image_count > 0
    logger.info(f'Image gallery loaded successfully')
