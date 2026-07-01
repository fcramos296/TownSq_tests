import pytest
from playwright.sync_api import expect
from pages.login_page import LoginPage
from utils.settings import settings


def _visible_count(locator):
    total = locator.count()
    visible = 0
    for i in range(total):
        try:
            if locator.nth(i).is_visible():
                visible += 1
        except Exception:
            continue
    return visible


def _has_visible_error(page):
    selectors = [
        "[role='alert']",
        ".alert",
        ".alert-danger",
        ".error",
        ".error-message",
        ".toast-error",
        "text=/inv[aá]lido/i",
        "text=/incorrect/i",
        "text=/error/i",
        "text=/senha/i",
        "text=/email/i",
    ]
    for sel in selectors:
        try:
            loc = page.locator(sel)
            for i in range(loc.count()):
                if loc.nth(i).is_visible():
                    return True
        except Exception:
            continue
    return False


@pytest.mark.e2e
@pytest.mark.smoke
class TestLoginPageUI:
    def test_login_page_loads(self, page, base_url):
        login_page = LoginPage(page)
        login_page.navigate_to_login(base_url)
        expect(page).to_have_url(base_url)

    def test_login_page_title(self, page, base_url):
        login_page = LoginPage(page)
        login_page.navigate_to_login(base_url)
        assert (
            "login" in page.title().lower()
            or "townsq" in page.title().lower()
            or "octadesk" in page.title().lower()
        )

    def test_username_field_is_visible(self, page, base_url):
        login_page = LoginPage(page)
        login_page.navigate_to_login(base_url)
        assert login_page.username() is not None

    def test_password_field_is_visible(self, page, base_url):
        login_page = LoginPage(page)
        login_page.navigate_to_login(base_url)
        assert login_page.password() is not None

    def test_submit_button_is_visible(self, page, base_url):
        login_page = LoginPage(page)
        login_page.navigate_to_login(base_url)
        assert login_page.submit() is not None

    def test_first_visit_shows_no_global_error(self, page, base_url, browser_context):
        isolated_context = browser_context.browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )
        isolated_page = isolated_context.new_page()
        try:
            isolated_page.goto(
                base_url,
                wait_until="networkidle",
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
    def test_empty_credentials_shows_error(self, page, base_url):
        login_page = LoginPage(page)
        login_page.navigate_to_login(base_url)
        login_page.click_submit()
        assert login_page.is_error_visible() or page.locator("input:invalid").count() > 0

    def test_invalid_email_format(self, page, base_url):
        login_page = LoginPage(page)
        login_page.navigate_to_login(base_url)
        login_page.fill_username("invalid-email")
        login_page.fill_password("somepassword")
        login_page.click_submit()
        assert login_page.is_error_visible() or page.locator("input:invalid").count() > 0

    def test_forgot_password_link_is_present(self, page, base_url):
        login_page = LoginPage(page)
        login_page.navigate_to_login(base_url)
        assert login_page.forgot_password() is not None

    def test_invalid_credentials_shows_error(self, page, base_url):
        login_page = LoginPage(page)
        login_page.navigate_to_login(base_url)
        login_page.perform_login("invalid_user@example.com", "wrong_password_123")
        assert login_page.is_error_visible() or _has_visible_error(page)


@pytest.mark.e2e
@pytest.mark.regression
class TestLoginFlow:
    @pytest.mark.skipif(not settings.USERNAME or not settings.PASSWORD, reason="Credentials not configured")
    def test_successful_login(self, page, base_url, credentials):
        login_page = LoginPage(page)
        login_page.navigate_to_login(base_url)
        login_page.perform_login(credentials["username"], credentials["password"])
        page.wait_for_load_state("networkidle")
        assert page.url != base_url
