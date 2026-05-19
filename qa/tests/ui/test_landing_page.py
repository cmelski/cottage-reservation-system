from qa.pages.landing import LandingPage
from playwright.sync_api import expect
from qa.utils.logging_utils import get_logger
logger = get_logger(__name__)


def test_landing_page(page_instance):
    landing_page = LandingPage(page_instance)
    expect(landing_page.heading_one).to_be_visible()
    expect(landing_page.heading_one).to_contain_text(landing_page.HEADING_ONE)
    logger.info(f'Landing Page loaded successfully. {landing_page.HEADING_ONE} is displayed')
