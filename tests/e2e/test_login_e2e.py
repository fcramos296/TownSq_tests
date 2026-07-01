import pytest
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError

from pages.login_page import LoginPage
from utils.settings import settings


@pytest.fixture
def login_page(page):
    return LoginPage(page)


def _has_visible_error(page) -> bool:
    candidates = [
        "div.toast-error",
        "[role='alert']",
        ".error",
        ".alert",
        "text=/erro|error|inv[áa]lido|invalid/i",
    ]

    for selector in candidates:
        try:
            page.wait_for_selector(selector, state="visible", timeout=2000)
            return True
        except PlaywrightTimeoutError:
            pass

    return False


@pytest.mark.e2e
@pytest.mark.smoke
class TestLoginPageUI:
    def test_login_page_loads(self, page, base_url, login_page):
        login_page.navigate_to_login(base_url)
        expect(page).to_have_url(base_url)

    def test_login_page_title(self, page, base_url, login_page):
        login_page.navigate_to_login(base_url)
        title = page.title().lower()
        assert "login" in title or "townsq" in title or "octadesk" in title

    def test_username_field_is_visible(self, page, base_url, login_page):
        login_page.navigate_to_login(base_url)
        locator = page.locator(login_page.USERNAME_INPUT)
        expect(locator.first).to_be_visible()

    def test_password_field_is_visible(self, page, base_url, login_page):
        login_page.navigate_to_login(base_url)
        locator = page.locator(login_page.PASSWORD_INPUT)
        expect(locator.first).to_be_visible()

    def test_submit_button_is_visible(self, page, base_url, login_page):
        login_page.navigate_to_login(base_url)
        locator = page.locator(login_page.SUBMIT_BUTTON)
        expect(locator.first).to_be_visible(timeout=settings.TIMEOUT)

    def test_first_visit_shows_no_global_error(self, page, base_url, browser_context):
        isolated_context = browser_context.browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )
        isolated_page = isolated_context.new_page()
        try:
            isolated_page.goto(
                base_url,
                wait_until="domcontentloaded",
                timeout=settings.TIMEOUT,
            )
            assert not _has_visible_error(
                isolated_page
            ), "Mensagem de erro visível no primeiro carregamento"
        finally:
            isolated_page.close()
            isolated_context.close()


@pytest.mark.e2e
@pytest.mark.negative
class TestLoginValidation:
    def test_empty_credentials_shows_error(self, page, base_url, login_page):
        login_page.navigate_to_login(base_url)
        login_page.click_submit()
        assert login_page.is_error_visible() or page.locator("input:invalid").count() > 0

    def test_invalid_email_format(self, page, base_url, login_page):
        login_page.navigate_to_login(base_url)
        login_page.fill_username("invalid-email")
        login_page.fill_password("somepassword")
        login_page.click_submit()
        assert login_page.is_error_visible() or page.locator("input:invalid").count() > 0

    def test_forgot_password_link_is_present(self, page, base_url, login_page):
        login_page.navigate_to_login(base_url)
        link = page.locator(login_page.FORGOT_PASSWORD_LINK)
        expect(link.first).to_be_visible(timeout=settings.TIMEOUT)


@pytest.mark.e2e
@pytest.mark.regression
class TestLoginFlow:
    @pytest.mark.skipif(
        not settings.USERNAME or not settings.PASSWORD,
        reason="Credentials not configured",
    )
    def test_successful_login(self, page, base_url, login_page, credentials):
        login_page.navigate_to_login(base_url)
        login_page.perform_login(credentials["username"], credentials["password"])
        assert page.url != base_url or page.locator("text=/dashboard|home|bem-vindo/i").count() > 0

    def test_invalid_credentials_shows_error(self, page, base_url, login_page):
        login_page.navigate_to_login(base_url)
        login_page.perform_login("invalid_user@example.com", "wrong_password_123")
        assert login_page.is_error_visible() or _has_visible_error(page)