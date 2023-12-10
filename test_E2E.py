from selenium import webdriver

def test_site_load():
    driver = webdriver.Chrome()
    driver.get('http://localhost:5000')
    assert "Login" in driver.title
