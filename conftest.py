import pytest
from playwright.sync_api import sync_playwright, expect, Page
from HomePage import HomePage

@pytest.fixture(scope='function')
def chronium_page() -> Page:
    "Inititialize page"
    with sync_playwright() as playwright:
        chronium = playwright.chromium.launch(headless=False)
        yield chronium.new_page()

@pytest.fixture(scope='function')
def playwright_chrome_page(chronium_page: Page) -> HomePage:
    "Initialize main class that we will use in our tests"
    expect.set_options(timeout=5000)
    return HomePage(chronium_page)

@pytest.fixture(scope='function')
def common_data() -> dict:
    "Returns common data that we will use in our tests"
    return {'url' : 'https://autofaq.ai/',
            'greeting' : 'Напишите свой вопрос и я постараюсь вам помочь',
            'input_placeholder' : 'Задайте свой вопрос...'
            }

@pytest.fixture(scope='function')
def benchmark_data():
    pass