from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.timeout = 30000

    def navigate(self, url: str):
        self.page.goto(url, timeout=self.timeout)

    def get_element(self, selector: str):
        return self.page.locator(selector)

    def click(self, selector: str):
        self.get_element(selector).click(timeout=self.timeout)

    def fill(self, selector: str, value: str):
        self.get_element(selector).fill(value, timeout=self.timeout)

    def wait_for_element(self, selector: str):
        self.page.wait_for_selector(selector, timeout=self.timeout)

    def is_visible(self, selector: str) -> bool:
        return self.get_element(selector).is_visible()

    def get_text(self, selector: str) -> str:
        return self.get_element(selector).inner_text(timeout=self.timeout)

    def expect_url(self, url: str):
        expect(self.page).to_have_url(url, timeout=self.timeout)
