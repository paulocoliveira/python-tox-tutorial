import pytest
import os
import random
from selenium.webdriver.common.by import By
from selenium import webdriver

lt_options = {
    "user": os.getenv("LT_USERNAME"),
    "accessKey": os.getenv("LT_ACCESS_KEY"),
    "build": os.getenv("BUILD_NAME", "Default Build"),
    "name": os.getenv("TEST_NAME", "Default Test"),
    "platformName": os.getenv("PLATFORM_NAME", "Windows 11"),
    "browserName": os.getenv("BROWSER_NAME", "Chrome"),
    "browserVersion": os.getenv("BROWSER_VERSION", "latest"),
    "selenium_version": os.getenv("SELENIUM_VERSION", "latest")
}

def generate_email():
    numbers = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    email = f"maria-costa-{numbers}@example.com"
    return email

@pytest.fixture
def browser():
    web_driver = webdriver.ChromeOptions() if lt_options["browserName"].lower() == "chrome" else webdriver.FirefoxOptions()
    web_driver.set_capability('LT:Options', lt_options)

    driver = webdriver.Remote(
        command_executor="https://hub.lambdatest.com/wd/hub",
        options=web_driver
    )
    
    driver.maximize_window()
    yield driver
    driver.quit()

def test_create_account(browser):
    browser.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/register")

    browser.find_element(By.ID, "input-firstname").send_keys("Maria")

    browser.find_element(By.ID, "input-lastname").send_keys("Costa")

    browser.find_element(By.ID, "input-email").send_keys(generate_email())

    browser.find_element(By.ID, "input-telephone").send_keys("+351123456789")

    browser.find_element(By.ID, "input-password").send_keys("987654321")

    browser.find_element(By.ID, "input-confirm").send_keys("987654321")

    browser.find_element(By.XPATH, "//label[@for='input-newsletter-yes']").click()

    browser.find_element(By.XPATH, "//label[@for='input-agree']").click()

    browser.find_element(By.XPATH, "//input[@value='Continue']").click()

    assert browser.title == "Your Account Has Been Created!"