from playwright.sync_api import expect

class LoginPage:
    USERNAME_INPUTS = [
        "input[type='email']",
        "input[name='email']",
        "input[name='username']",
        "input[id*='email' i]",
        "input[placeholder*='email' i]",
        "input[placeholder*='login' i]",
    ]

    PASSWORD_INPUTS = [
        "input[type='password']",
        "input[name='password']",
        "input[id*='password' i]",
        "input[placeholder*='password' i]",
        "input[placeholder*='senha' i]",
    ]

    SUBMIT_BUTTONS = [
        "button[type='submit']",
        "input[type='submit']",
        "button:has-text('Login')",
        "button:has-text('Entrar')",
        "button:has-text('Acessar')",
        "button:has-text('Sign in')",
    ]

    FORGOT_PASSWORD_LINKS = [
        "a:has-text('Forgot password')",
        "a:has-text('Esqueci')",
        "a:has-text('Recuperar senha')",
        "a[href*='password']",
        "a[href*='forgot']",
    ]

    ERROR_SELECTORS = [
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

    def __init__(self, page):
        self.page = page

    def navigate_to_login(self, base_url):
        self.page.goto(base_url, wait_until="networkidle")

    def _first_visible(self, selectors):
        for sel in selectors:
            loc = self.page.locator(sel)
            if loc.count() > 0:
                for i in range(loc.count()):
                    if loc.nth(i).is_visible():
                        return loc.nth(i)
        return None

    def username(self):
        return self._first_visible(self.USERNAME_INPUTS)

    def password(self):
        return self._first_visible(self.PASSWORD_INPUTS)

    def submit(self):
        return self._first_visible(self.SUBMIT_BUTTONS)

    def forgot_password(self):
        return self._first_visible(self.FORGOT_PASSWORD_LINKS)

    def fill_username(self, value):
        el = self.username()
        assert el is not None, "Campo de usuário/email não encontrado"
        el.fill(value)

    def fill_password(self, value):
        el = self.password()
        assert el is not None, "Campo de senha não encontrado"
        el.fill(value)

    def click_submit(self):
        el = self.submit()
        assert el is not None, "Botão de login não encontrado"
        el.click()

    def perform_login(self, username, password):
        self.fill_username(username)
        self.fill_password(password)
        self.click_submit()

    def is_error_visible(self):
        for sel in self.ERROR_SELECTORS:
            loc = self.page.locator(sel)
            for i in range(loc.count()):
                if loc.nth(i).is_visible():
                    return True
        return False
