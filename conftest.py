import os
import pytest
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()



def pytest_configure(config):
    config.option.htmlpath = "reports/report.html"
    config.option.self_contained_html = True


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://townsq.octadesk.com/login")


@pytest.fixture(scope="session")
def credentials():
    return {
        "username": os.getenv("USERNAME", ""),
        "password": os.getenv("PASSWORD", ""),
    }


@pytest.fixture(scope="session")
def browser_context(request):
    headed = request.config.getoption("headed")
    browser_name = request.config.getoption("browser") or "chromium"
    slowmo = request.config.getoption("slowmo")

    with sync_playwright() as p:
        browser_type = getattr(p, browser_name)
        browser = browser_type.launch(headless=not headed, slow_mo=slowmo)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        yield context
        context.close()
        browser.close()


@pytest.fixture(scope="function")
def page(browser_context):
    page = browser_context.new_page()
    yield page
    page.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            screenshot_dir = "reports/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            path = os.path.join(screenshot_dir, f"{item.nodeid.replace('::', '_').replace('/', '_')}.png")
            page.screenshot(path=path)
