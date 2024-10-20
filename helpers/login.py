# helpers/login.py
'''Helper functions to automate the login process and set up the delivery form.'''
import logging
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (NoSuchElementException,
                                        TimeoutException, WebDriverException)
from selenium.webdriver.common.action_chains import ActionChains
from config import (USERNAME, PASSWORD, COMPANY_CODE, URL,
                    BUSINESS_NAME, SUPPLIER_NAME, DELIVERY_DATE, REFERENCE_NUMBERS)

logger = logging.getLogger(__name__)
logger.propagate = False

def login_sequence(driver):
    """
    Automates the login process to the application using configuration settings.

    Args:
        driver (webdriver): The Selenium WebDriver instance.

    Returns:
        None
    """
    try:
        driver.get(URL)
        driver.maximize_window()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(text(),'Log In by User')]"))).click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "companyCode"))
        ).send_keys(COMPANY_CODE)  # Replace with config.COMPANY_CODE if using environment variables
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "userName"))
        ).send_keys(USERNAME)  # Replace with config.USERNAME
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "web-input-189fl3qekkb5c7yp"))
        ).send_keys(PASSWORD)  # Replace with config.PASSWORD
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Sign In')]"))).click()
        logger.info("Login successful.")

        # Click "Purchasing" menu button
        purchasing_menu_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "nav-group-btn-110")))
        purchasing_menu_button.click()
        # Click "Deliveries" option
        deliveries_option = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//span[@id='nav-action-name-10103899' and contains(text(), 'Deliveries')]",
                )
            )
        )
        deliveries_option.click()
        logger.info("Login complete.")
    except (NoSuchElementException, TimeoutException, WebDriverException) as e:
        logger.error("An error occurred during login: %s", e, exc_info=True)
        traceback.print_exc()
        raise

def click_got_it_button(driver):
    """
    Clicks the 'Got It' button to dismiss any introductory modals or notifications.
    """
    try:
        # Updated XPath to ensure it targets the correct 'Got It' button
        got_it_span_xpath = "//span[contains(@class, 'ng-scope') and contains(text(), 'Got It')]"
        # Wait until the 'Got It' button is clickable
        got_it_span = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, got_it_span_xpath)))
        # Use ActionChains to click the button
        ActionChains(driver).move_to_element(got_it_span).pause(1).click(got_it_span).perform()
        logger.info("'Got It' button clicked successfully.")
    except TimeoutException as te:
        logger.error("Timeout while trying to click 'Got It' button: %s", te, exc_info=True)
    except (NoSuchElementException, WebDriverException) as e:
        print(f"Failed to click 'Got It' button: {e}")
        traceback.print_exc()

def select_business(driver):
    """Selects a business from the dropdown menu."""
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "select_value_label_syn_web-md-select-sktwiwwhlaqys9zi"))).click()
    search_bar = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "web-input-sktwiwwhlaqys9zk")))
    search_bar.clear()
    search_bar.send_keys(BUSINESS_NAME)
    business_option_xpath = f"//md-option//span[contains(text(), '{BUSINESS_NAME}')]"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, business_option_xpath))).click()
    print(f"Business '{BUSINESS_NAME}' selected successfully.")

def select_delivery(driver):
    """
    Selects the delivery option from the menu.
    """
    try:
        deliveries_text = WebDriverWait(driver, timeout=50).until(EC.element_to_be_clickable((
                By.XPATH, "//div[@class='md-text ng-binding' and contains(text(), 'Deliveries')]")))
        deliveries_text.click()
        logger.info("Clicked on '%s' text.", 'Deliveries')
        delivery_option = WebDriverWait(driver, timeout=50).until(
            EC.element_to_be_clickable((By.XPATH, "//md-option[.//div[text()='Deliveries']]")))
        delivery_option.click()
        logger.info("Delivery option '%s' selected successfully.", 'Deliveries')
    except (NoSuchElementException, TimeoutException, WebDriverException) as e:
        logger.error("Failed to select delivery option '%s': %s", 'Deliveries', e, exc_info=True)
        traceback.print_exc()

def select_carryout(driver):
    """Selects the carryout supplier and clicks the plus button."""
    try:
        # Click the 'Select a Supplier' dropdown to open it
        supplier_dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//md-select[@id='select-supplier']")))
        supplier_dropdown.click()
        print("Supplier dropdown menu found and clicked.")

        # Wait for the supplier option to become clickable and click it
        supplier_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//md-option[.//div[text()='{SUPPLIER_NAME}']]")))
        supplier_option.click()
        print(f"Supplier '{SUPPLIER_NAME}' selected successfully.")

        # Click the 'plus' button to add the supplier
        plus_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='web-md-button-189fl5zekkb7r6i4']")))
        plus_button.click()
        print("Plus button found and clicked.")

    except TimeoutException as e:
        print(f"Timeout occurred while selecting carryout supplier or clicking plus button: {e}")
    except NoSuchElementException as e:
        print(f"Element not found during the carryout supplier selection: {e}")
    except (WebDriverException) as e:
        print(f"An error occurred in select_carryout: {e}")
    finally:
        print("Entering Form")

def set_up(driver):
    """Maximizes the window using the fullscreen button and sets up the delivery date, 
    clicking the background after each date entry."""

    try:
        # Maximize the window
        full_screen_button = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'md-icon-button') and @aria-label='Full Screen']")))
        full_screen_button.click()
        print("Window maximized successfully.")

        # Set date 1
        date_input1 = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, "web-md-datepicker-189fl7m7kkbbu567-syn-input-id")))
        driver.execute_script("arguments[0].removeAttribute('readonly')", date_input1)
        date_input1.clear()
        date_input1.send_keys(DELIVERY_DATE)
        print(f"Date 1 set to: {DELIVERY_DATE}")

        # Set date 2
        date_input2 = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, "web-md-datepicker-189fl7mhkkbbupq7-syn-input-id")))
        driver.execute_script("arguments[0].removeAttribute('readonly')", date_input2)
        date_input2.clear()
        date_input2.send_keys(DELIVERY_DATE)
        print(f"Date 2 set to: {DELIVERY_DATE}")

        # Wait until the input field is visible and clickable
        reference_input = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "yourRef")))
        reference_input = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "yourRef")))

        # Clear any existing text and enter the reference number
        reference_input.clear()
        reference_input.send_keys(REFERENCE_NUMBERS)
        print(f"Reference number set to: {REFERENCE_NUMBERS}")

    except (NoSuchElementException,TimeoutException, WebDriverException) as e:
        print(f"Failed to set details: {e}")
