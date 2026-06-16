import json
import sys
import uuid
from pathlib import Path
import logging
logger = logging.getLogger(__name__)
import pytest
import os
import time
import datetime
from datetime import datetime, date
import shutil



from playwright.sync_api import sync_playwright
from qa.business_logic.db_queries.db_queries import *
from qa.core.config.environment import load_environment
from qa.core.db.db_client_metrics import DBClientMetrics
from qa.core.db.db_client import DBClient
from qa.core.api.api_client import APIClient

test_results = []
test_start = {}
run_start_time = None


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


@pytest.fixture()
def load_env_config():
    environment = os.environ.get('ENV_NAME')
    with open(f'qa/tests/config/{environment}_env.json') as f:
        config = json.load(f)
    return config
# return the BASE_URL from the loaded .env file for use in tests
@pytest.fixture
def url_start(load_env_config):
    base_url = load_env_config['ui']['base_url']
    return base_url

# allure results directory setup - clean before test run and create if doesn't exist
def pytest_sessionstart(session):
    # exit after collecting list of test cases
    # pytest --collect-only -q > test_cases.txt

    if "--collect-only" in sys.argv:
        return

    # load the current automation env (default is --env=test)
    load_environment(
        session.config.getoption("--env")
    )

    # load all test cases

    db_client_metrics = DBClientMetrics()
    db_client_metrics.load_test_cases()

    # set up allure reporting

    allure_dir = Path("qa/allure-results")
    if allure_dir.exists():
        shutil.rmtree(allure_dir)
    allure_dir.mkdir(parents=True, exist_ok=True)

    conn = DBClientMetrics()
    cur = conn.cursor
    scope = session.config.getoption("--scope")
    build_version = session.config.getoption("--build-version")

    cur.execute("""
        INSERT INTO test_runs (run_date, build_version, run_scope, total_tests)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """, (
        date.today(),
        build_version,
        scope,
        0  # placeholder for now
    ))

    session.config.run_id = cur.fetchone()[0]

    conn.commit()
    conn.close()


def pytest_collection_finish(session):
    session.config.total_tests = len(session.items)


# Log test start times for duration calculation later
def pytest_runtest_logstart(nodeid, location):
    # called when test starts
    test_start[nodeid] = {
        "start_time": datetime.now().isoformat()
    }


# This hook is called before each test phase (setup, call, teardown).
def pytest_runtest_setup(item):
    item.trace_id = str(uuid.uuid4())
    logger.info(f"▶ Starting {item.name}")
    logger.info(f" TRACE={item.trace_id}")
    item.start_time = time.perf_counter()


# Log skipped and xfailed tests with details
def pytest_runtest_logreport(report):
    if report.skipped:
        logger.info(f"SKIPPED: {report.nodeid} - {report.longrepr}")
    elif report.outcome == "xfailed":
        logger.info(f"XFAIL: {report.nodeid} - {report.longrepr}")

    assertion_error = ''
    if report.when == "call":
        node_id = report.nodeid
        if report.failed:
            # extract only the assertion message
            if hasattr(report.longrepr, "reprcrash"):
                assertion_error = report.longrepr.reprcrash.message.split('\n')[0]
        else:
            assertion_error = 'N/A'
        test_results.append({
            "test_name": report.nodeid,
            "result": report.outcome.upper(),
            "error": assertion_error,
            "test_start": test_start[node_id]['start_time'],
            "test_end": datetime.now().isoformat(),
            "duration": report.duration
        })


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # only care about actual test execution
    if report.when == "call":

        # safe duration
        duration = time.perf_counter() - getattr(item, "start_time", time.perf_counter())

        status = "passed" if report.passed else "failed"

        if report.failed and call.excinfo:
            # logger.error(f"FAILED: {item.name}")
            logger.error(
                f"FAILED TEST: {item.nodeid}",
                exc_info=call.excinfo._excinfo
            )

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

            try:
                conn = DBClientMetrics()
                cur = conn.cursor

                cur.execute("""
                    SELECT * FROM test_cases
                    WHERE name = %s;
                    """, (item.nodeid,))  # <-- pass as tuple

                test_case = cur.fetchone()
                area = test_case[3]
                test_case_id = test_case[0]

                cur.execute("""
                       INSERT INTO defects (
                           created_date,
                           severity,
                           area,
                           test_case_id
                       )
                       VALUES (%s, %s, %s, %s)
                   """, (
                    date.today(),
                    'Medium',
                    area,
                    test_case_id
                ))

                conn.commit()

            except Exception as e:
                print(f"DB INSERT FAILED: {e}")

            finally:
                conn.close()

        else:
            logger.info(f"PASSED: {item.name}")

        try:
            conn = DBClientMetrics()
            cur = conn.cursor

            cur.execute("""
                        INSERT INTO test_case_results (
                            run_id,
                            test_name,
                            duration_seconds,
                            status,
                            trace_id
                        )
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                item.config.run_id,
                item.nodeid,
                duration,
                status,
                item.trace_id
            ))

            conn.commit()

        except Exception as e:
            print(f"DB INSERT FAILED: {e}")

        finally:
            conn.close()


def pytest_sessionfinish(session, exitstatus):
    conn = DBClientMetrics()
    cur = conn.cursor

    cur.execute("""
            UPDATE test_runs
            SET total_tests = %s
            WHERE id = %s
        """, (
        len(session.items),
        session.config.run_id
    ))

    conn.commit()
    conn.close()

    data = {
        "test_run_results": test_results
    }

    with open("qa/logs/pass_fail_log.json", "w") as f:
        json.dump(data, f, indent=2)


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
def db_client(request):
    trace_id = request.node.trace_id
    db_client = DBClient(trace_id=trace_id)
    yield db_client
    db_client.close()



@pytest.fixture()
def api_client(request, load_env_config):
    trace_id = request.node.trace_id
    endpoints = load_env_config['api']
    base_url = load_env_config['ui']['base_url']
    api_client = APIClient(base_url=base_url, trace_id=trace_id, config=endpoints)
    return api_client


@pytest.fixture()
def reset_db(db_client, load_env_config):

    db_tables_to_clean = load_env_config['database']['reset_tables']
    db_client.reset_db_tables(db_tables_to_clean)
    logger.info('Resetting DB')
    # populate required tables
    with open('qa/business_logic/data/new_cottage_details.json') as f:
        cottage_details = json.load(f)['cottage_info']
    add_cottage_to_db(cottage_details, db_client)


# main tests fixture that yields page object
# and then closes context and browser after yield as part of teardown
@pytest.fixture(scope="function")
def page_instance(request, url_start):
    logger.info(f'Using BASE_URL: {url_start}')
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
