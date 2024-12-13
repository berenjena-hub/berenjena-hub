from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from core.environment.host import get_host_for_selenium_testing
from core.selenium.common import initialize_driver, close_driver
import time


def wait_for_page_to_load(driver, timeout=4):
    WebDriverWait(driver, timeout).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )


def test_follow_unfollow_sequence():
    driver = initialize_driver()

    try:
        host = get_host_for_selenium_testing()

        driver.get(f"{host}/login")
        wait_for_page_to_load(driver)
        driver.find_element(By.ID, "email").send_keys("user3@example.com")
        driver.find_element(By.ID, "password").send_keys("1234")
        driver.find_element(By.ID, "submit").click()
        time.sleep(1)
        driver.find_element(By.LINK_TEXT, "Sample dataset 6").click()
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, 800);")
        time.sleep(1)
        driver.find_element(By.LINK_TEXT, "Doe, Jane").click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        print("Pasado")

    except Exception as e:
        print("No pasado:", e)

    finally:
        close_driver(driver)


# Llama a la prueba
test_follow_unfollow_sequence()
