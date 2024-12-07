import time
from selenium.webdriver.common.by import By


from core.environment.host import get_host_for_selenium_testing
from core.selenium.common import initialize_driver


class TestSeleniumDataset:
    
    def setup_method(self):
        self.driver = initialize_driver()
        self.vars = {}

    def teardown_method(self):
        self.driver.quit()
        
    def test_file_content(self):
        self.driver.get(get_host_for_selenium_testing())
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        self.driver.find_element(By.ID, "email").send_keys("user2@example.com")
        self.driver.find_element(By.ID, "password").send_keys("1234")
        self.driver.find_element(By.ID, "submit").click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Sample dataset 3").click()
        time.sleep(1)
        self.driver.find_element(By.PARTIAL_LINK_TEXT, "Download all").click()
        time.sleep(1)
        self.driver.find_element(By.PARTIAL_LINK_TEXT, "Explore more datasets").click()
        time.sleep(1)
        self.driver.back()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//button[@onclick=\"copyText('text_cite')\"]").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//button[@onclick=\"copyText('apa_cite')\"]").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//button[@onclick=\"copyText('ris_cite')\"]").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//button[@onclick=\"copyText('bibtex_cite')\"]").click()
        time.sleep(1)
        element = self.driver.find_element(By.XPATH, "//div[@class='col-md-8 col-12']")
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//div[@class='col-md-8 col-12']//a").click()
        time.sleep(1)
        self.driver.back()
        self.driver.find_element(By.PARTIAL_LINK_TEXT, "Download Glencoe").click()
        time.sleep(1)
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//a[@href='https://doi.org/10.1016/j.jss.2024.112150']").click()
        time.sleep(5)
        
        