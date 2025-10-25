# test_modals.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Fixture pour le navigateur
@pytest.fixture(params=["chrome", "firefox", "edge"])
def browser(request):
    if request.param == "chrome":
        driver = webdriver.Chrome()
    elif request.param == "firefox":
        driver = webdriver.Firefox()
    elif request.param == "edge":
        driver = webdriver.Edge()
    else:
        raise ValueError("Navigateur non supporté")
    
    driver.maximize_window()
    yield driver
    driver.quit()


# Test modale Download the Game
def test_modal_download_game(browser):
    browser.get("http://127.0.0.1:5000")  # adapte l'URL de test
    download_button = browser.find_element(By.ID, "download-button")
    download_button.click()
    modal = WebDriverWait(browser, 5).until(
        EC.visibility_of_element_located((By.ID, "download-modal"))
    )
    assert modal.is_displayed()
    overlay = browser.find_element(By.ID, "modal-overlay")
    overlay.click()
    time.sleep(0.5)
    assert not modal.is_displayed()


# Test modales miniatures
@pytest.mark.parametrize("thumbnail_id", [
    "thumb1",
    "thumb2",
    "thumb3",
    "thumb4"
])
def test_modal_thumbnails(browser, thumbnail_id):
    browser.get("http://127.0.0.1:5000")
    thumb = browser.find_element(By.ID, thumbnail_id)
    thumb.click()
    modal = WebDriverWait(browser, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "thumbnail-modal"))
    )
    assert modal.is_displayed()
    overlay = browser.find_element(By.ID, "modal-overlay")
    overlay.click()
    time.sleep(0.5)
    assert not modal.is_displayed()


# Test profil joueur en tête du classement
def test_modal_top_player_profile(browser):
    browser.get("http://127.0.0.1:5000")
    top_player = browser.find_element(By.CSS_SELECTOR, ".leaderboard .player:first-child")
    top_player.click()
    modal = WebDriverWait(browser, 5).until(
        EC.visibility_of_element_located((By.ID, "player-profile-modal"))
    )
    assert modal.is_displayed()
    overlay = browser.find_element(By.ID, "modal-overlay")
    overlay.click()
    time.sleep(0.5)
    assert not modal.is_displayed()
