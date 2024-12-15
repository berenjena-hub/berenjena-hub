
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


from core.environment.host import get_host_for_selenium_testing
from core.selenium.common import initialize_driver


class TestSeleniumFile:
    
    def setup_method(self):
        self.driver = initialize_driver()
        self.vars = {}

    def teardown_method(self):
        self.driver.quit()
        
    def test_file_content(self):
        self.driver.get(get_host_for_selenium_testing())
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        self.driver.find_element(By.ID, "email").send_keys("user1@example.com")
        self.driver.find_element(By.ID, "password").send_keys("1234")
        self.driver.find_element(By.ID, "submit").click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Sample dataset 5").click()
        time.sleep(1)
        button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'file5.uvl')]")
        button.click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "fileViewerModal"))
        )
        content_element = self.driver.find_element(By.ID, "fileContent")

        assert content_element.text.strip() != "", "El contenido del archivo no se muestra correctamente."
        
        copy_button = self.driver.find_element(By.XPATH, "//button[contains(@onclick, 'copyToClipboard()')]")
        copy_button.click()
        time.sleep(1)

        file_content = self.driver.find_element(By.ID, "fileContent").text
        assert file_content.strip() != "", "El contenido del archivo no se puede copiar."
        time.sleep(1)
        download_button = self.driver.find_element(By.ID, "downloadButton")
        download_button.click()
        time.sleep(1)
        
        check_button = self.driver.find_element(By.XPATH, "//button[contains(@class, 'btn-primary') and contains(@class, 'dropdown-toggle')]")
        check_button.click()

        time.sleep(1)
        
        try:
            uvl_option = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.LINK_TEXT, "UVL"))
            )
            ActionChains(self.driver).move_to_element(uvl_option).click().perform()
            time.sleep(3) 
            print("Interacción con UVL completada.")
        except Exception as e:
            with open("debug_dom.html", "w") as f:
                f.write(self.driver.page_source)
                raise AssertionError(f"Error al interactuar con UVL: {str(e)}")
            
        check_button = self.driver.find_element(By.XPATH, "//button[contains(@class, 'btn-outline-primary') and normalize-space()='Check']")
        check_button.click()

        time.sleep(1)
        
        syntax_check_option = self.driver.find_element(By.LINK_TEXT, "Syntax check")

        syntax_check_option.click()
        time.sleep(1)
        assert "Syntax check" in self.driver.page_source, "Error al realizar la verificación de sintaxis."
        
        time.sleep(1)
        button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'file11.uvl')]")
        button.click()
        
        time.sleep(1)
        button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'file5.uvl')]")
        button.click()
        
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Sample dataset 5").click()
        time.sleep(1)
