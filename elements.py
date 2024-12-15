from base_elements import BaseElements
import allure
import datetime

class Button(BaseElements):
    """Class to represent buttons"""
    def has_type(self) -> str:
        return 'button'

class Window(BaseElements):
    """Class to represent windows"""
    def has_type(self) -> str:
        return 'widget window'

class Input(BaseElements):
    """Class to represent inputs"""
    def has_type(self) -> str:
        return 'input'

    def fill(self, value: str) -> None:
        "Fill text to given locator"
        with allure.step('Fill to = {}, with name =  {}, value = {} '.format(self.has_type, self.name, value)):
            locator = self.get_locator()
            locator.fill(value)

    def locator_found_by_placeholder(self, placeholder: str) -> None:
        "Check that we can found locator by text"
        with allure.step('Checking = {}, with name = {}, has placeholder = {}'.format(self.has_type, self.name, placeholder)):
            locator = self.page.get_by_placeholder(placeholder)
            self.check_if_available(locator)

class Text(BaseElements):
    """Class to represent texts"""

    def has_type(self) -> str:
        return 'text'

class Messages(BaseElements):
    """Class to represent messages"""

    def has_type(self):
        return 'messages'

    def if_buttons_clickable(self, message_id: str) -> None:
        "Insures that buttons are clickable"
        locators = self.page.locator(f"//div[@id='{message_id}']{self.locator}//button").all()
        for locator in locators:
            self.check_if_enabled(locator)

    def if_buttons_not_clickable(self, message_id: str) -> None:
        "Insures that buttons are NOT clickable"
        locators = self.page.locator(f"//div[@id='{message_id}']{self.locator}//button").all()
        for locator in locators:
            self.check_if_disabled(locator)

    def get_id_of_last_message(self) -> str:
        "Returns id: str of the last element in a given locator"
        with allure.step('Finding last Id of = {}, with name = {}'.format(self.has_type(), self.name)):
            locator = self.get_locator().all()[-1]
            return locator.get_attribute('id')

    def check_name(self, message_id: str, name: str) -> None:
        "Insures that given message has certain name"
        with allure.step('Finding name of an element by id = {}, name text = {}'.format(self.has_type(),  self.name)):
            child = self.page.get_by_text(name, exact=True).and_(self.get_locator())
            parent = self.page.locator(f"//div[@id = '{message_id}']").filter(has=child)
            self.check_if_available(parent)

    def has_avatar(self, message_id: str) -> None:
        "Insures that given message has certain avatar"
        with allure.step('Finding avatar of an element by id = {}'.format(message_id)):
            child = self.get_locator()
            parent = self.page.locator(f"//div[@id = '{message_id}']").filter(has=child)
            self.check_if_available(parent)

    def check_data(self, message_id, data: datetime) -> None:
        "Insures that given message has certain date (dd mmm yyyy)"
        with allure.step('Finding data of an element by id = {}'.format(message_id)):
            child = self.page.get_by_text(data.strftime("%H:%M:%S, %d %B %Y"))
            parent = self.page.locator(f"//div[@id = '{message_id}']").filter(has=child)
            self.check_if_available(parent)

    def check_status(self, message_id: str) -> None:
        "Insures that given message has certain status"
        with allure.step('Finding status of an element by id = {}'.format(message_id)):
            child = self.get_locator()
            parent = self.page.locator(f"//div[@id = '{message_id}']").filter(has=child)
            self.check_if_available(parent)


class Icon(BaseElements):
    """Class to represent icons"""

    def has_type(self) -> str:
        return 'icon'