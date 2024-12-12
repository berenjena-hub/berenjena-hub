from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.environment.host import get_host_for_selenium_testing
from core.selenium.common import initialize_driver, close_driver

def test_dashboard_title_exists():
    driver = initialize_driver()
    try:
        host = get_host_for_selenium_testing()
        driver.get(f'{host}/dashboard')
        try:
            title_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "dashboard-title"))
            )
        except TimeoutException:
            raise AssertionError('Test failed! No se encontró el título del dashboard.')
    finally:
        close_driver(driver)

def test_dashboard_card_exists():
    driver = initialize_driver()
    try:
        host = get_host_for_selenium_testing()
        driver.get(f'{host}/dashboard')
        try:
            card_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".card"))
            )
        except TimeoutException:
            raise AssertionError('Test failed! No se encontró ninguna tarjeta en el dashboard.')
    finally:
        close_driver(driver)

def test_dashboard_title_color():
    driver = initialize_driver()
    try:
        host = get_host_for_selenium_testing()
        driver.get(f'{host}/dashboard')
        try:
            title_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "dashboard-title"))
            )
            title_color = title_element.value_of_css_property("color")
            expected_color = "rgba(0, 0, 0, 1)"  # Ajusta según tu CSS real
            if title_color != expected_color:
                raise AssertionError(f'Test failed! El color del título no es el esperado. Se obtuvo: {title_color}')
        except TimeoutException:
            raise AssertionError('Test failed! No se encontró el título del dashboard.')
    finally:
        close_driver(driver)

def test_dashboard_user_datasets_count_visible():
    driver = initialize_driver()
    try:
        host = get_host_for_selenium_testing()
        driver.get(f'{host}/dashboard')
        try:
            user_datasets_count = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "user-datasets-count"))
            )
            text = user_datasets_count.text
            if not text.isdigit():
                raise AssertionError(f'Test failed! El conteo de datasets no es un número válido: {text}')
        except TimeoutException:
            raise AssertionError('Test failed! No se encontró el elemento con el conteo de datasets del usuario.')
    finally:
        close_driver(driver)

def test_dashboard_feature_models_count():
    driver = initialize_driver()
    try:
        host = get_host_for_selenium_testing()
        driver.get(f'{host}/dashboard')
        try:
            fm_count = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "feature-models-count"))
            )
            text = fm_count.text
            if not text.isdigit():
                raise AssertionError(f'Test failed! El conteo de feature models no es un número válido: {text}')
        except TimeoutException:
            raise AssertionError('Test failed! No se encontró el elemento con el conteo de feature models.')
    finally:
        close_driver(driver)

def test_dashboard_layout_integrity():
    driver = initialize_driver()
    try:
        host = get_host_for_selenium_testing()
        driver.get(f'{host}/dashboard')
        try:
            container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".dashboard-container"))
            )
            width = container.value_of_css_property("width")
            if not width:
                raise AssertionError('Test failed! No se obtuvo el ancho del contenedor. El layout podría no estar cargado correctamente.')
        except TimeoutException:
            raise AssertionError('Test failed! No se encontró el contenedor principal del dashboard.')
    finally:
        close_driver(driver)
