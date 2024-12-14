import time
from selenium.webdriver.common.by import By
from core.environment.host import get_host_for_selenium_testing
from core.selenium.common import initialize_driver


class Testtype():

  def setup_method(self, method):
    self.driver = initialize_driver()
    self.vars = {}

  def teardown_method(self, method):
    self.driver.quit()

  def test_testauthor(self):
    self.driver.get(get_host_for_selenium_testing())
    self.driver.maximize_window()
    time.sleep(1)
    self.driver.find_element(By.CSS_SELECTOR, ".sidebar-item:nth-child(3) .align-middle:nth-child(2)").click()
    time.sleep(1)
    
    
    self.driver.find_element(By.CSS_SELECTOR, "#publication_type > option:nth-child(4)").click()
    time.sleep(1)
    self.driver.find_element(By.ID, "apply-filters").click()
    time.sleep(1)
    
    self.driver.find_element(By.CSS_SELECTOR, "#publication_type > option:nth-child(2)").click()
    time.sleep(1)
    self.driver.find_element(By.ID, "apply-filters").click()
    time.sleep(1)
    
    self.driver.find_element(By.CSS_SELECTOR, "#publication_type > option:nth-child(8)").click()
    time.sleep(1)
    self.driver.find_element(By.ID, "apply-filters").click()
    time.sleep(1)
    
    self.driver.find_element(By.LINK_TEXT, "Sample dataset 1").click()
    time.sleep(1)
    self.driver.find_element(By.ID, "search").click()
    time.sleep(1)