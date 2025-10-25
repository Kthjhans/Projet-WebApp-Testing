import pytest
import sys
import os

# === Correction pour pytest-xdist ===
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import app  # Flask app

# =========================
# Fixtures Flask
# =========================
@pytest.fixture(scope="module")
def client():
    """Fixture Flask test client pour les tests backend."""
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test_secret"
    with app.test_client() as client:
        yield client


# =========================
# Fixtures Selenium
# =========================
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

BROWSERS = ["chrome", "firefox", "edge"]

@pytest.fixture(params=BROWSERS)
def browser(request):
    """Fixture dynamique Selenium WebDriver pour Chrome, Firefox et Edge."""
    driver = None
    if request.param == "chrome":
        opts = ChromeOptions()
        opts.add_argument("--headless")  # facultatif, supprimer pour voir le navigateur
        driver = webdriver.Chrome(options=opts)
    elif request.param == "firefox":
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        driver = webdriver.Firefox(options=opts)
    elif request.param == "edge":
        opts = EdgeOptions()
        opts.add_argument("--headless")
        driver = webdriver.Edge(options=opts)

    yield driver
    driver.quit()
