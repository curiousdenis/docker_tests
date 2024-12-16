import allure
import pytest
from playwright.sync_api import sync_playwright, expect, Page
from HomePage import HomePage


@pytest.fixture(scope='function')
def chronium_page() -> Page:
    "Inititialize page"
    with sync_playwright() as playwright:
        chronium = playwright.chromium.launch(headless=True)
        context = chronium.new_context(record_video_dir="allure_results/")
        yield context.new_page()

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
    "For the benchmark backend testing"
    pass

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call = 'call'):
    "To generate image and video for failed tests"
    report = yield
    page = item.funcargs['chronium_page']
    if report.get_result().outcome == 'failed':
        allure.attach(page.screenshot(), name = 'Screenshot_error', attachment_type= allure.attachment_type.PNG)
        video_path = page.video.path()
        page.context.close()
        allure.attach(open(video_path, 'rb').read(),name=f"Video_error", attachment_type=allure.attachment_type.WEBM)