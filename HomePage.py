from base_page import BasePage
from elements import Icon, Window, Input, Button, Text, Messages
from dataclasses import dataclass, field
from datetime import datetime
from playwright.sync_api import Page

class HomePage(BasePage):
    """Main page"""
    def __init__(self, page):
        self.widget = Widget(page)
        super().__init__(page)

class Widget:
    """
    Main element that we will test
    it will store:
        1 - elements of widet as instance attributes
        2 - main methods, such:
            a - send user form
            b - send main text
            c - recieve text
    """
    def __init__(self, page : Page):
        self.page = page
        self.widget_window = WidgetWindow(page)
        self.widget_user_form = WidgetUserForm(page)
        self.widget_dialog_window = WidgetDialogWindow(page)
        self.widget_prompt = WidgetInputField(page)
        self.current_length = 0
        self.send_messages = dict()

    def send_user_form(self, name: str, email: str) -> None:
        "Method to send user form"
        self.widget_user_form.send(name, email)

    def create_message(self, text: str, reciever: str, sender: str = 'UNDENIFIED_USER') -> str:
        "Here we will send send message, store this message, increase current length by 1 and return id of sended message"
        self.current_length = len(self.widget_dialog_window.messages.get_locator().all())
        time = self.widget_prompt.send(text)
        self.widget_dialog_window.messages.locator_has_not_length(self.current_length)
        self.current_length += 1
        id = self.widget_dialog_window.messages.get_id_of_last_message()
        self.send_messages[id] = Message(sender, reciever, time, text)
        return id

    def replies_received_to_message(self, message_id: str) -> str:
        "We will search for a recieved message from chat-bot and append this id to the main message from user and return id of founded message"
        self.widget_dialog_window.messages.locator_has_not_length(self.current_length)
        id = self.widget_dialog_window.messages.get_id_of_last_message()
        self.send_messages[message_id].replies_ids.append(id)
        self.current_length = len(self.widget_dialog_window.messages.get_locator().all())
        return id

    def make_checks_for_message(self, message_id: str, recieve: bool = False, sender: str = None) -> None:
        "Here we make all necessary cheks for a message - we can add other if needed"
        if recieve:
            self.widget_dialog_window.name.check_name(message_id, sender)
            self.widget_dialog_window.avatar.has_avatar(message_id)
        else:
            self.widget_dialog_window.status_done.check_status(message_id)
            # self.widget_dialog_window.message.check_data(message_id, self.send_messages[message_id].when_sent)

class WidgetWindow:
    """Subclass for Widget - to store all methods and locators of Window"""
    def __init__(self, page: Page):
        self.page = page
        self.icon = Icon(page, locator = '//div[@id= "chat21-launcher-button"]', name = 'widget icon')
        self.widget = Window(page, locator = '//div[@id = "chat21-conversations"]', name = 'widget window')
        self.closing_icon = Icon(page, locator = '//a[@class = "chat21-sheet-header-close-button"]'
                                 , name = 'closing widget icon')
        self.status = 'Closed'
    def open_widget(self) -> None:
        "Method to open widget and store current status of it"
        self.icon.click_element()
        if self.status == 'Closed':
            self.widget.check_if_available()
            self.status = 'Opened'
        elif self.status == 'Opened':
            self.widget.check_if_hidden()
            self.status = 'Closed'

    def click_closing_icon(self) -> None:
        "Method to click closing icon inside widget"
        self.closing_icon.click_element()
        self.status = 'Closed'

    def resize_widget(self):
        pass


class WidgetUserForm:
    """Subclass for Widget - to store all methods and locators of User Form in Widget"""
    def __init__(self, page):
        self.form_panel = Input(page, locator='//div[@class= "form_panel"]', name = 'user form panel')
        self.personal_name = Input(page, locator='//input[@name = "senderFullName"]', name='form user name')
        self.personal_email = Input(page, locator='//input[@name = "senderEmail"]', name='form user email')
        self.personal_send_button = Button(page, locator='//div[@class = "form_panel_actions"]//button',
                                           name='form user info submit')

    def send(self, name, email):
        "Send user's name and email to widget form"
        self.personal_name.fill(name)
        self.personal_email.fill(email)
        self.personal_send_button.click_element()
        self.form_panel.locator_has_length(0)


class WidgetDialogWindow:
    """Subclass for Widget - to store all methods and locators of Dialog Window"""

    def __init__(self, page):
        self.page = page
        self.greeting = Text(page, locator ='//div[@class = "chat21-header-modal-select"]//div',
                             name = 'greeting after first attempt')
        self.messages = Messages(page, locator = '//div[@class = "msg_block msg_block-last"]', name = 'messages')
        self.name = Messages(page, locator = "//div[@class = 'message_sender_fullname']", name = 'message name')
        self.avatar = Messages(page, locator = "//div[@class = 'content-avatar']", name = 'message avatar')
        self.status_done = Messages(page, locator = "//div[@class = 'icon f21ico-done']", name = 'message status')
        self.link_buttons = Messages(page, locator = '//div[@class = "msg_container base_receive buttons"]',
                                     name = 'message buttons')

class WidgetInputField:
    """Subclass for Widget - to store all methods and locators of Input in Widget"""

    def __init__(self, page):
        self.prompt_field = Input(page, locator = '//textarea[@id= "chat21-main-message-context"]', name = 'prompt placeholder')
        self.button_send = Button(page, locator = '//div[@id = "chat21-button-send"]', name = 'send button')

    def find_input_by_placeholder(self, placeholder):
        "Method to check if a given locator has certain plcaholder"
        self.prompt_field.locator_found_by_placeholder(placeholder)

    def send(self, text):
        "Main method to send data"
        self.prompt_field.click_element()
        self.prompt_field.fill(text)
        self.button_send.click_element()
        return datetime.now()

@dataclass(frozen=True)
class Message:
    """
    It is a dataclass to represent Message, since there is only data ordinary class is not needed
    dataclass/collections.namedtuple/typing.Namedtuple will be enough
    dataclasses is superior, those i chose it
    """
    who_send : str
    who_receieved : str
    when_sent : datetime
    text : str
    replies_ids : list[str] = field(default_factory=list)
