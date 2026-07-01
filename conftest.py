import os
import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from utils.settings import settings


@pytest.fixture(scope="session")
def base_url():
    return settings.BASE_URL


@pytest.fixture(scope="session")
def credentials():
    return {
        "username": settings.USERNAME,
        "password": settings.PASSWORD,
    }


@pytest.fixture(scope="session")
def browser_context(request):
    cli_headed = request.config.getoption("headed")
    browser_name = request.config.getoption("browser") or settings.BROWSER
    slowmo = request.config.getoption("slowmo")
    headless = False if cli_headed else settings.HEADLESS

    with sync_playwright() as p:
        browser_type = getattr(p, browser_name)
        browser = browser_type.launch(
            headless=headless,
            slow_mo=slowmo,
        )
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        yield context
        context.close()
        browser.close()


@pytest.fixture(scope="function")
def page(browser_context):
    page = browser_context.new_page()
    page.set_default_timeout(settings.TIMEOUT)
    yield page
    page.close()


@pytest.fixture
def login_page(page, base_url):
    login = LoginPage(page)
    login.navigate_to_login(base_url)
    return login


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            screenshot_dir = "reports/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            path = os.path.join(
                screenshot_dir,
                f"{item.nodeid.replace('::', '_').replace('/', '_')}.png",
            )
            page.screenshot(path=path)