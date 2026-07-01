from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME_INPUT = "input#email, input[name='email'], input[type='email']"
    PASSWORD_INPUT = "input#password, input[name='password'], input[type='password']"
    SUBMIT_BUTTON = "button[type='submit'], button:has-text('Sign in'), button:has-text('Entrar')"
    FORGOT_PASSWORD_LINK = "a:has-text('Forgot password'), a:has-text('Esqueci')"
    ERROR_MESSAGE = "[role='alert'], .error, .error-message, .alert-danger"

    def navigate_to_login(self, base_url):
        self.navigate(base_url, wait_until="domcontentloaded")

    def username_field(self):
        return self.page.locator(self.USERNAME_INPUT).first

    def password_field(self):
        return self.page.locator(self.PASSWORD_INPUT).first

    def submit_button(self):
        return self.page.locator(self.SUBMIT_BUTTON).first

    def forgot_password_link(self):
        return self.page.locator(self.FORGOT_PASSWORD_LINK).first

    def error_message(self):
        return self.page.locator(self.ERROR_MESSAGE).first

    def fill_username(self, value):
        self.fill(self.username_field(), value)

    def fill_password(self, value):
        self.fill(self.password_field(), value)

    def click_submit(self):
        self.click(self.submit_button())

    def perform_login(self, username, password):
        self.fill_username(username)
        self.fill_password(password)
        self.click_submit()

    def is_error_visible(self, timeout=5000):
        try:
            self.wait_visible(self.error_message(), timeout=timeout)
            return True
        except Exception:
            return False