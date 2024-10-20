# helpers/utilities.py
'''Helper functions for various utility operations.'''
import logging
import traceback
from selenium import webdriver
import openpyxl
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (NoSuchElementException, TimeoutException, WebDriverException,
                                        ElementClickInterceptedException, StaleElementReferenceException)
from config import BROWSER, DRIVER_PATH

logger = logging.getLogger(__name__)
logger.propagate = False

def initialize_driver():
    """
    Initializes the Selenium WebDriver based on configuration settings.
    Returns:
        webdriver.Edge: The initialized WebDriver instance.
    """
    try:
        if BROWSER.lower() == "edge":
            options = Options()
            options.use_chromium = True
            service = Service(executable_path=DRIVER_PATH)
            driver = webdriver.Edge(service=service, options=options)
            driver.maximize_window()
            logger.info("Edge WebDriver initialized and window maximized.")
            return driver
        else:
            logger.warning("Unsupported browser specified. Defaulting to Edge.")
            return initialize_driver()
    except WebDriverException as e:
        logger.error("Failed to initialize WebDriver: %s", e, exc_info=True)
        return None

def close_driver(driver):
    """
    Closes the Selenium WebDriver.
    Args:
        driver (webdriver.Edge): The Selenium WebDriver instance.
    """
    try:
        if driver:
            driver.quit()
            logger.info("WebDriver closed.")
        else:
            logger.warning("No WebDriver to close.")
    except Exception as e:
        logger.error("Failed to close WebDriver: %s", e, exc_info=True)
        raise

def close_form(driver):
    """
    Closes the modal dialog that appears after processing a product.
    Args:
        driver (webdriver): The Selenium WebDriver instance.
    Returns:
        bool: True if the modal was closed successfully, False otherwise.
    """
    try:
        WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.ID, "web-md-button-189fl7nukkbbymuc")))
        close_button = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, "web-md-button-189fl7nukkbbymuc")))
        close_button.click()
        logger.info("Clicked the X button.")
        return True
    except TimeoutException:
        logger.error("Submit button was not clickable after %s seconds.", 50)
        traceback.print_exc()
        return False

def save_form(driver):
    """
    Clicks the 'Save' button on the web form.
    Args:
        driver (webdriver): The Selenium WebDriver instance.
    Returns:
        None
    """
    try:
        save_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "web-md-button-189fl7lckkbbqvow")))
        driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
        save_button.click()
        logger.info("Save button clicked successfully.")
    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException,
        StaleElementReferenceException) as e:
        logger.error("Failed to click Save button: '%s", e, exc_info=True)

# # # For transient errors (like network glitches), implement a retry mechanism.
# def retry_click(driver, by, identifier, retries=3, delay=2):
#     """
#     Attempts to click an element multiple times before failing.
#     Args:
#         driver (webdriver): The Selenium WebDriver instance.
#         by (By): Selenium locator strategy.
#         identifier (str): The identifier for the locator.
#         retries (int): Number of retry attempts.
#         delay (int): Delay between retries in seconds.
#     Returns:
#         bool: True if clicked successfully, False otherwise.
#     """
#     for attempt in range(retries):
#         try:
#             element = WebDriverWait(driver, 10).until(
#                 EC.element_to_be_clickable((by, identifier))
#             )
#             element.click()
#         except (NoSuchElementException, TimeoutException, WebDriverException):
#             logger.error("Failed to click '%s' after '%s' attempts.", attempt + 1, identifier)
#             time.sleep(delay)
#             logger.error("Failed to click '%s' after '%s' attempts.", identifier, retries)

# def retry(func, retries=3, delay=2, *args, **kwargs):
#     """
#     Retries a function upon failure.
#     Args:
#         func (callable): The function to retry.
#         retries (int): Number of retries.
#         delay (int | float): Delay between retries in seconds.
#     Returns:
#         Any: The result of the function if successful.
#     Raises:
#         Exception: The last exception raised if all retries fail.
#     """
#     for attempt in range(1, retries + 1):
#         try:
#             return func(*args, **kwargs)
#         except Exception as e:
#             logger.warning("Attempt %s failed with error: %s", attempt, e)
#             if attempt == retries:
#                 logger.error("All %s attempts failed.", retries)
#                 raise
#             pause(delay)
