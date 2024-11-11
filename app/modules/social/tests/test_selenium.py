from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        driver.find_element(By.NAME, "email").send_keys("user2@example.com")
        driver.find_element(By.NAME, "password").send_keys("1234")
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
        wait_for_page_to_load(driver)
        time.sleep(2)

        user_id = 65
        driver.get(f"{host}/profile/other?user_id={user_id}")
        wait_for_page_to_load(driver)
        time.sleep(2)

        follow_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[style*='lightgreen']")))
        follow_button.click()
        print("Le has dado a Follow")
        time.sleep(4)

        WebDriverWait(driver, 5).until(EC.staleness_of(follow_button))
        time.sleep(2)

        unfollow_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[style*='lightcoral']")))
        unfollow_button.click()
        print("Le has dado a Unfollow")
        time.sleep(4)

        print("Pasado")

    except Exception as e:
        print("No pasado:", e)

    finally:
        close_driver(driver)


# Llama a la prueba
test_follow_unfollow_sequence()
