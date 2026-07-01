from playwright.sync_api import Page, expect


class LoginPage:
    ERROR_MESSAGE = "[role='alert'], .error, .alert, text=/erro|error|inv[áa]lido|invalid/i"
    USERNAME_INPUT = "input[name='username'], input[type='email'], input#username"
    PASSWORD_INPUT = "input[name='password'], input[type='password'], input#password"
    SUBMIT_BUTTON = "button[type='submit'], button:has-text('Entrar'), button:has-text('Sign in')"
    FORGOT_PASSWORD_LINK = "a:has-text('Esqueci'), a:has-text('Forgot password')"

    def __init__(self, page: Page):
        self.page = page

    def navigate_to_login(self, base_url: str) -> None:
        self.page.goto(base_url, wait_until="domcontentloaded")

    def fill_username(self, username: str) -> None:
        self.page.locator(self.USERNAME_INPUT).first.fill(username)

    def fill_password(self, password: str) -> None:
        self.page.locator(self.PASSWORD_INPUT).first.fill(password)

    def click_submit(self) -> None:
        self.page.locator(self.SUBMIT_BUTTON).first.click()

    def perform_login(self, username: str, password: str) -> None:
        self.fill_username(username)
        self.fill_password(password)
        self.click_submit()

    def has_visible_error(self) -> bool:
        locator = self.page.locator(self.ERROR_MESSAGE)
        try:
            return locator.first.is_visible()
        except Exception:
            return False

    def is_error_visible(self) -> bool:
        return self.has_visible_error()

    def forgot_password_link_visible(self) -> bool:
        locator = self.page.locator(self.FORGOT_PASSWORD_LINK)
        try:
            return locator.first.is_visible()
        except Exception:
            return False

    def assert_loaded(self) -> None:
        expect(self.page.locator(self.USERNAME_INPUT).first).to_be_visible()
        expect(self.page.locator(self.PASSWORD_INPUT).first).to_be_visible()
        expect(self.page.locator(self.SUBMIT_BUTTON).first).to_be_visible()