# test_selenium_fixt_params.py
import pytest
from selenium import webdriver

@pytest.fixture(params=["chrome", "firefox", "edge"])
def browser(request):
    if request.param == "chrome":
        driver = webdriver.Chrome()
    elif request.param == "firefox":
        driver = webdriver.Firefox()
    elif request.param == "edge":
        driver = webdriver.Edge()
    else:
        raise ValueError(f"Unsupported browser {request.param}")
    
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


def test_homepage_title(browser):
    browser.get("http://127.0.0.1:5000")
    assert "Welcome" in browser.title


def test_login_page_exists(browser):
    browser.get("http://127.0.0.1:5000/login")
    assert "Login" in browser.page_source
