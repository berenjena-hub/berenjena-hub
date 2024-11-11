from selenium.common.exceptions import NoSuchElementException
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

from core.environment.host import get_host_for_selenium_testing
from core.selenium.common import initialize_driver, close_driver

class TestNotePadActions:
    def setup_method(self, method):
        self.driver = initialize_driver()
        self.vars = {}

    def teardown_method(self, method):
        close_driver(self.driver)
    
    def test_createnotepad(self):
        self.driver.get(f"{get_host_for_selenium_testing()}/login")
        time.sleep(2)
        self.driver.set_window_size(912, 1011)
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys("user1@example.com")
        self.driver.find_element(By.ID, "password").send_keys("1234")
        self.driver.find_element(By.ID, "submit").click()
        time.sleep(2)
        self.driver.get(f"{get_host_for_selenium_testing()}/notepad/create")
        time.sleep(2)
        self.driver.find_element(By.ID, "title").click()
        self.driver.find_element(By.ID, "title").send_keys("n1")
        self.driver.find_element(By.ID, "body").click()
        self.driver.find_element(By.ID, "body").send_keys("n1")
        self.driver.find_element(By.ID, "submit").click()

def test_notepad_index():
    driver = initialize_driver()
    try:
        host = get_host_for_selenium_testing()
        driver.get(f'{host}/notepad')
        time.sleep(4)  # Wait to make sure the page has loaded
    finally:
        close_driver(driver)

# You can define more test cases here
