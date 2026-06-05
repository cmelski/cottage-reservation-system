import json
import random
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
import pytest
import os
import time
from faker import Faker
from datetime import timedelta

# load env file variables
from dotenv import load_dotenv

from playwright.sync_api import sync_playwright
from qa.business_logic.db_queries.queries import *
from qa.business_logic.data.new_booking import NewBooking


# define test run parameters
# in terminal you can run for e.g. 'pytest test_web_framework_api.py --browser_name firefox'
def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="browser selection"
    )

    parser.addoption(
        "--url_start", action="store", default="test", help="starting url for UI tests"
    )

    parser.addoption(
        "--env", action="store", default="test", help="Environment to run tests against")

    parser.addoption(
        "--build-version", action="store", default="unknown", help="Build version for test run tracking"
    )

    parser.addoption(
        "--scope", action="store", default="single", help="test run scope - single, subset, smoke, regression, full"
    )


# load corresponding .env file based on --env parameter (e.g. test.env, staging.env, prod.env)
@pytest.fixture(scope="session", autouse=True)
def env(request):
    env_name = request.config.getoption("--env")

    # This gets the directory where conftest.py lives
    project_root = Path(__file__).resolve().parent

    env_path = project_root / f"{env_name}.env"

    print("Loading from:", env_path)

    load_dotenv(env_path, override=True)

    print("BASE_URL:", os.getenv("BASE_URL"))


# return the BASE_URL from the loaded .env file for use in tests
@pytest.fixture
def url_start():
    return os.getenv("BASE_URL", "http://127.0.0.1:5002/")


# This hook is called before each test phase (setup, call, teardown).
def pytest_runtest_setup(item):
    logger.info(f"▶ Starting {item.name}")
    item.start_time = time.perf_counter()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()

    # only care about actual test execution
    if report.when == "call":

        if report.failed:
            logger.error(f"FAILED: {item.name}")

            if "page_instance" in item.funcargs:
                page = item.funcargs["page_instance"]

                screenshot_dir = Path("qa/logs/screenshots")
                screenshot_dir.mkdir(
                    parents=True,
                    exist_ok=True
                )

                path = screenshot_dir / f"{item.name}.png"
                page.screenshot(path=path)

                logger.info(
                    f"Screenshot saved: {path}"
                )

            else:
                logger.warning(
                    "No page fixture found for screenshot"
                )

        else:
            logger.info(f"PASSED: {item.name}")


@pytest.fixture
def context(browser):
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True)
    yield context
    context.tracing.stop(path="qa/logs/trace.zip")
    context.close()


# remove logging noise from faker module
def pytest_configure():
    logging.getLogger("faker").setLevel(logging.WARNING)


@pytest.fixture()
def create_single_booking():
    new_booking = NewBooking()
    return new_booking.generate_new_reservation_details()


@pytest.fixture()
def create_multiple_bookings():
    new_booking = NewBooking()
    return [new_booking.generate_new_reservation_details() for i in range(10)]


@pytest.fixture()
def api_config_loader():
    with open('qa/business_logic/config/api_config.json') as f:
        config_data = json.load(f)
    return config_data


@pytest.fixture()
def reset_db():
    with open('qa/business_logic/config/db_tables.json') as f:
        db_tables = json.load(f)
    # purge tables
    tables = db_tables['tables']
    clean_db_tables(tables)
    # populate required tables
    with open('qa/business_logic/data/new_cottage_details.json') as f:
        cottage_details = json.load(f)['cottage_info']
    add_cottage_to_db(cottage_details)


# main tests fixture that yields page object
# and then closes context and browser after yield as part of teardown
@pytest.fixture(scope="function")
def page_instance(request, url_start):
    browser_name = request.config.getoption("browser_name")
    headed = request.config.getoption("headed")
    headless = not headed

    with sync_playwright() as p:
        if browser_name == "chrome":
            browser = p.chromium.launch(headless=headless)
        elif browser_name == "firefox":
            browser = p.firefox.launch(headless=headless)

        # state = "qa/auth_state_test.json" if os.path.exists("qa/auth_state_test.json") else None

        # if state:
        #     context = browser.new_context(storage_state=state)
        # else:
        #     context = browser.new_context()

        context = browser.new_context()

        page = context.new_page()

        page.goto(url_start)

        logger.info('Launching UI...')

        try:
            # auto accept javascript alerts
            page.on("dialog", lambda dialog: dialog.accept())
            yield page
        finally:
            context.close()
            browser.close()
