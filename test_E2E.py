import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(2)
    yield driver
    driver.quit()


def create_test_user(driver):
    driver.get("http://localhost:5000/login")
    driver.find_element(By.NAME, "username").send_keys("testuser")
    driver.find_element(By.NAME, "password").send_keys("testpassword")
    driver.find_element(By.XPATH, "//input[@type='submit'][@value='Login']").click()
    driver.implicitly_wait(4)


    if driver.current_url.endswith("/login"):        

        driver.get("http://localhost:5000/signup")
        driver.find_element(By.NAME, "username").send_keys("testuser")
        driver.find_element(By.NAME, "email").send_keys("testuser@example.com")
        driver.find_element(By.NAME, "password").send_keys("testpassword")
        driver.find_element(By.XPATH, "//input[@type='submit'][@value='Signup']").click()
        driver.implicitly_wait(4)

        driver.get("http://localhost:5000/login")
        driver.find_element(By.NAME, "username").send_keys("testuser")
        driver.find_element(By.NAME, "password").send_keys("testpassword")
        driver.find_element(By.XPATH, "//input[@type='submit'][@value='Login']").click()


def test_end_to_end(driver):
    # Connexion
    create_test_user(driver)

    # Search Bar
    search_box = driver.find_element(By.NAME, "query")
    search_box.send_keys("margarita")
    search_box.send_keys(Keys.RETURN)
    assert "Margarita" in driver.page_source


    # Swipe page

    swipe_link = driver.find_element(By.XPATH, "//a[@href='/swipe']")
    swipe_link.click()
  

    # Liker et ne pas liker des cocktails
    like_button = driver.find_element(By.CLASS_NAME, "like-button")
    like_button.click()

    driver.implicitly_wait(1)

    pass_button = driver.find_element(By.CLASS_NAME, "pass-button")
    pass_button.click()

    # See favorites
    driver.find_element(By.XPATH, "//a[@href='/favorites']").click()
    assert "Vos Cocktails Favoris" in driver.page_source


    # Se déconnecter
    driver.find_element(By.XPATH, "//a[@href='/profile']").click()
    assert "Profil" in driver.page_source

    driver.implicitly_wait(10)
    
    driver.find_element(By.ID, "logout-button").click()

    driver.implicitly_wait(5)

    assert "Login" in driver.title
