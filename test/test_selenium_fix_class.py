# test_selenium_fix_class.py
import pytest
from selenium import webdriver

@pytest.fixture(scope="class")
def browser(request):
    # Choix du navigateur ici : Chrome par défaut
    driver = webdriver.Chrome()  # ChromeDriver doit être installé
    driver.implicitly_wait(5)
    
    # Associer le driver à la classe de test
    request.cls.driver = driver
    yield
    driver.quit()


@pytest.mark.usefixtures("browser")
class TestHomePage:
    
    def test_homepage_title(self):
        self.driver.get("http://127.0.0.1:5000")
        assert "Welcome" in self.driver.title

    def test_login_page_exists(self):
        self.driver.get("http://127.0.0.1:5000/login")
        assert "Login" in self.driver.page_source
