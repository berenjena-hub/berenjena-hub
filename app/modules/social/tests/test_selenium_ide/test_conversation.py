# Generated by Selenium IDE
import time
from selenium.webdriver.common.by import By
from core.environment.host import get_host_for_selenium_testing
from core.selenium.common import initialize_driver


class TestCommentdataset():
    def setup_method(self, method):
        self.driver = initialize_driver()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_commentdataset(self):
        self.driver.get(get_host_for_selenium_testing())
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        self.driver.find_element(By.ID, "email").send_keys("user3@example.com")
        self.driver.find_element(By.ID, "password").send_keys("1234")
        self.driver.find_element(By.ID, "submit").click()
        time.sleep(1)
        self.driver.get(get_host_for_selenium_testing() + "/social")
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, "li.friend-item[data-id='122']").click()
        time.sleep(2)
        self.driver.find_element(By.ID, "message-input").click()
        self.driver.find_element(By.ID, "message-input").send_keys("Esto es una prueba de Selenium")
        self.driver.find_element(By.ID, "send-button").click()
        time.sleep(2)
        self.driver.get(get_host_for_selenium_testing() + "/logout")
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        self.driver.find_element(By.ID, "email").send_keys("user4@example.com")
        self.driver.find_element(By.ID, "password").send_keys("1234")
        self.driver.find_element(By.ID, "submit").click()
        time.sleep(1)
        self.driver.get(get_host_for_selenium_testing() + "/social")
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, "li.friend-item[data-id='121']").click()
        time.sleep(2)
        self.driver.find_element(By.ID, "message-input").click()
        self.driver.find_element(By.ID, "message-input").send_keys("Esto es una prueba de Selenium")
        self.driver.find_element(By.ID, "send-button").click()
        time.sleep(2)
