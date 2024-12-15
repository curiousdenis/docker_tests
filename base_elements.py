from abc import ABC, abstractmethod
import allure
from playwright.sync_api import Page, Locator, expect

class BaseElements(ABC):
    """It is an abstract class for Elements that will be inherited and not instantiated"""
    def __init__(self, page: Page, name : str, locator = None) -> None:
        self.page = page
        self.locator = locator
        self.name = name

    @abstractmethod
    def has_type(self) -> str:
        "All class that will inherit from abstract have to override this method"
        return 'baseelements'

    def get_locator(self) -> Locator:
        "Method to return Locator by (usually) XPATH"
        locator = self.locator.format()
        return self.page.locator(locator)


    def click_element(self) -> None:
        "First get locator then click element"
        with allure.step('Clicking = {}, with name = {}'.format(self.has_type, self.name)):
            locator = self.get_locator()
            locator.click()

    def check_if_available(self, external_locator: Locator = None) -> None:
        "Assert that givin locator is visible"
        with allure.step('Checking = {}, with name = {} is avaliable'.format(self.has_type, self.name)):
            if external_locator:
                locator = external_locator
            else:
                locator = self.get_locator()
            expect(locator).to_be_visible()

    def check_if_enabled(self, external_locator: Locator = None) -> None:
        "Assert that givin locator is enabled"
        with allure.step('Checking = {}, with name = {} is enabled'.format(self.has_type, self.name)):
            if external_locator:
                locator = external_locator
            else:
                locator = self.get_locator()
            expect(locator).to_be_enabled()

    def check_if_disabled(self, external_locator: Locator = None) -> None:
        "Assert that givin locator is disabled"
        with allure.step('Checking = {}, with name = {} is enabled'.format(self.has_type, self.name)):
            if external_locator:
                locator = external_locator
            else:
                locator = self.get_locator()
            expect(locator).to_be_disabled()

    def check_if_hidden(self, external_locator: Locator = None) -> None:
        "Assert that givin locator is hidden"
        with allure.step('Checking =  {}, with name = {} is hidden'.format(self.has_type, self.name)):
            if external_locator:
                locator = external_locator
            else:
                locator = self.get_locator()
            expect(locator).to_be_hidden()

    def locator_has_length(self, length: int) -> None:
        "Insures that number of given locators is equivalent to giving length"
        with allure.step('Checking = {}, with name = {}, that it has lengh = {}'.format(self.has_type, self.name, length)):
            locator = self.get_locator()
            expect(locator).to_have_count(length, timeout=60_000)

    def locator_has_not_length(self, length: int) -> None:
        "Insures that number of given locators is NOT equivalent to giving length"
        with allure.step('Checking = {}, with name = {}, does not has length = {}'.format(self.has_type, self.name, length)):
            locator = self.get_locator()
            expect(locator).not_to_have_count(length, timeout=60_000)

    def validate_text(self, value: str) -> None:
        "Insures that given locator has given text"
        with allure.step('Checking = {}, with name = {}, has text = {}'.format(self.has_type, self.name, value)):
            locator = self.get_locator()
            expect(locator).to_have_text(value)