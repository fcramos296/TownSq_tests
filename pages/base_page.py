from utils.settings import settings


class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate(self, url, wait_until="domcontentloaded"):
        self.page.goto(url, wait_until=wait_until, timeout=settings.TIMEOUT)
        self.page.wait_for_load_state(wait_until)

    def click(self, locator):
        locator.wait_for(state="visible", timeout=settings.TIMEOUT)
        locator.click()

    def fill(self, locator, value):
        locator.wait_for(state="visible", timeout=settings.TIMEOUT)
        locator.fill(value)

    def wait_visible(self, locator, timeout=None):
        locator.wait_for(state="visible", timeout=timeout or settings.TIMEOUT)
        return locator