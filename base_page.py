from playwright.sync_api import Page
import allure
class BasePage:
    """It is a class that will be used by other Pages"""
    def __init__(self, page : Page) -> None:
        self.page = page

    def website(self, url: str) -> None:
        "Open a website with given url"
        with allure.step('Opening the url = {}'.format(url)):
            self.page.goto(url, wait_until='domcontentloaded')

    def reload(self) -> None:
        "Reload page"
        self.page.reload()

    def clean_cookie(self):
        pass