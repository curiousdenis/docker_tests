import pytest

"""
1st step
    Write test cases and wrap in Pytest:
            Frontend - Playwright
            Backend - No frameworks (probably write simple ones)
    OOP, Page object pattern
    Some of test cases supposed to failed for the 2nd step
2nd step
    Docker the result of which Allure doc
"""

class TestWidget:
    """
    Class to store test methods that we will run:
        1 - normal testing: pytest tests.py
        2 - to benchmark use insted: pytest tests.py -m simple_benchmark_pool -v -s
    """
    @staticmethod
    @pytest.mark.parametrize('name, email', [('Denis', 'test@mail.ru')])
    def test_positive_user_first_attempt(common_data, playwright_chrome_page, name, email):
        "Positive test case where we: goto url, open widget, and send user data in a form (name and email) and do some checks"
        playwright_chrome_page.website(common_data['url'])
        playwright_chrome_page.widget.widget_window.open_widget()
        playwright_chrome_page.widget.send_user_form(name, email)
        playwright_chrome_page.widget.widget_dialog_window.greeting.validate_text(common_data['greeting'])
        playwright_chrome_page.widget.widget_prompt.find_input_by_placeholder(common_data['input_placeholder'])
        playwright_chrome_page.widget.widget_dialog_window.messages.locator_has_length(0)

    @staticmethod
    @pytest.mark.parametrize('prompt, reciever_name', [('Цены', 'autofaq')])
    def test_positive_user_prompt(common_data, playwright_chrome_page, prompt, reciever_name):
        "Positive test case where we: goto url, open widget, and send text and wait till we recieved an asnwer (any)"
        playwright_chrome_page.website(common_data['url'])
        playwright_chrome_page.widget.widget_window.open_widget()
        message_1 = playwright_chrome_page.widget.create_message(prompt, reciever_name)
        playwright_chrome_page.widget.replies_received_to_message(message_1)
        playwright_chrome_page.widget.make_checks_for_message(message_1)
        for recieve in playwright_chrome_page.widget.send_messages[message_1].replies_ids:
            playwright_chrome_page.widget.make_checks_for_message(recieve, recieve = True, sender = reciever_name)

    @staticmethod
    @pytest.mark.parametrize('prompt, reciever_name', [('Цены', 'autofaq')])
    def test_after_reload_test_not_disappear(common_data, playwright_chrome_page, prompt, reciever_name):
        "Case: to check that we still have the same conversation after page reload and nothing is missing"
        playwright_chrome_page.website(common_data['url'])
        playwright_chrome_page.widget.widget_window.open_widget()
        message_1 = playwright_chrome_page.widget.create_message(prompt, reciever_name)
        playwright_chrome_page.widget.replies_received_to_message(message_1)
        messages_num = playwright_chrome_page.widget.current_length
        playwright_chrome_page.reload()
        playwright_chrome_page.widget.widget_window.status = 'Closed'
        playwright_chrome_page.widget.widget_window.open_widget()
        playwright_chrome_page.widget.widget_dialog_window.messages.locator_has_length(messages_num)

    @staticmethod
    def test_widget_closing(common_data, playwright_chrome_page):
        "Case: we close widget by closing icon or clicking click again on opening widget icon"
        playwright_chrome_page.website(common_data['url'])
        playwright_chrome_page.widget.widget_window.open_widget()
        playwright_chrome_page.widget.widget_window.open_widget()
        playwright_chrome_page.widget.widget_window.open_widget()
        playwright_chrome_page.widget.widget_window.click_closing_icon()
        playwright_chrome_page.widget.widget_window.open_widget()

    @staticmethod
    @pytest.mark.parametrize('prompt, reciever_name', [('Меню', 'autofaq')])
    def test_buttons_to_be_clickable_that_will_fail(common_data, playwright_chrome_page, prompt, reciever_name):
        "Test case that will fail - insure that buttons are not clickable"
        playwright_chrome_page.website(common_data['url'])
        playwright_chrome_page.widget.widget_window.open_widget()
        message_1 = playwright_chrome_page.widget.create_message(prompt, reciever_name)
        message_2 = playwright_chrome_page.widget.replies_received_to_message(message_1)
        message_3 = playwright_chrome_page.widget.create_message(prompt, reciever_name)
        message_4 = playwright_chrome_page.widget.replies_received_to_message(message_3)
        playwright_chrome_page.widget.widget_dialog_window.link_buttons.if_buttons_clickable(message_2)

    @staticmethod
    def send_data(playwright_chrome_page, prompt, reciever_name):
        "Method that will be used by a benchmark"
        msg = playwright_chrome_page.widget.create_message(prompt, reciever_name)
        playwright_chrome_page.widget.replies_received_to_message(msg)


    @staticmethod
    @pytest.mark.simple_benchmark_pool
    @pytest.mark.benchmark(min_rounds=5)
    def test_benchmark_for_menu(benchmark, common_data, playwright_chrome_page):
        "Benchmark - to time how long it will take to recieve answer from chat bot if prompt = 'Меню'"
        playwright_chrome_page.website(common_data['url'])
        playwright_chrome_page.widget.widget_window.open_widget()
        benchmark(TestWidget.send_data, playwright_chrome_page, 'Меню', 'autofaq')

    @staticmethod
    @pytest.mark.simple_benchmark_pool
    @pytest.mark.benchmark(min_rounds=5)
    def test_benchmark_for_price(benchmark, common_data, playwright_chrome_page):
        "Benchmark - to time how long it will take to recieve answer from chat bot if prompt = 'Цены'"
        playwright_chrome_page.website(common_data['url'])
        playwright_chrome_page.widget.widget_window.open_widget()
        benchmark(TestWidget.send_data, playwright_chrome_page, 'Цены', 'autofaq')
