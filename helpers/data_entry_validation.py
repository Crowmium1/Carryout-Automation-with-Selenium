# helpers/data_entry_validation.py
'''Functions for data entry and form filling'''
import logging
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (NoSuchElementException, TimeoutException,
                                        WebDriverException)

logger = logging.getLogger(__name__)

def fill_fields(driver, fill_data):
    """
    Fills in the web form fields based on the DataFrame row data.
    Args:
        driver (webdriver): The Selenium WebDriver instance.
        row_data (pd.Series): The DataFrame row data.
    Returns:
        bool: True if fields are filled successfully, False otherwise.
    """
    try:
        quantity = int(fill_data["Qty"])
        cost_per_unit = int(fill_data["Cost per Unit"])
        logger.info("Filling fields: Qty=%s, Cost per Unit=%s", quantity, cost_per_unit)
        quantity_input = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, "web-input-189fl7q9kkbc4430-0")))
        quantity_input.clear()
        quantity_input.send_keys(str(quantity))
        unit_cost_input = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, "web-input-189fl7q9kkbc4436-0")))
        unit_cost_input.clear()
        unit_cost_input.send_keys(str(cost_per_unit))
        return True
    except (NoSuchElementException, TimeoutException) as e:
        logger.error("An error occurred while filling fields: %s", e, exc_info=True)
        traceback.print_exc()
        return False

def get_total_costs(driver, df, row_index):
    """
    Validates the total cost from the DataFrame against the 
    total cost displayed on the web table.
    Updates the DataFrame with new values.
    """
    try:
        total_cost_df = float(df.loc[row_index, "Total Cost"])
        logger.info("Expecting Total Cost: %s", total_cost_df)
        total_cost_xpath = "//td[contains(@class, 'text-right no-white-space-wrap md-cell ng-binding ng-scope') and not(contains(., 'context.viewQuantityOrdered'))]"
        total_cost_element = WebDriverWait(driver, timeout=20).until(EC.visibility_of_element_located((By.XPATH, total_cost_xpath)))
        total_cost_text = total_cost_element.text.strip().replace(",", "")
        total_cost_web = float(total_cost_text)
        logger.info("Total Cost encountered: '%s'", total_cost_web)
    except (NoSuchElementException, TimeoutException, WebDriverException) as e:
        logger.error("An unexpected error occurred: %s", e, exc_info=True)
        traceback.print_exc()
    return total_cost_df, total_cost_web

def extract_all_cells(driver, table_xpath, timeout=20):
    """
    Extracts all cell texts from all rows within a specified table in a modal dialog.
    Returns:
        list of dict: A list of dictionaries containing cell texts for each row.
    """
    try:
        # Wait for the modal container to be visible
        modal_container = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='md-dialog-container ng-scope']")))
        table = modal_container.find_element(By.XPATH, table_xpath)
        rows = table.find_elements(By.XPATH, ".//tr[contains(@class, 'md-row')]")
        all_data = []
        for index, row in enumerate(rows, start=1):
            cells = row.find_elements(By.XPATH, ".//td")
            cell_texts = [cell.text.strip() for cell in cells]
            # Map cell texts to a dictionary with keys. Otherwise this would be a
            # list of lists containing cell texts for each row.
            row_data = {
                'Product Code': cell_texts[1] if len(cell_texts) > 1 else '',
                'Product': cell_texts[2] if len(cell_texts) > 2 else '',
            }
            all_data.append(row_data)
        return all_data
    except Exception as e:
        logger.error("An error occurred while extracting all cells: %s", e, exc_info=True)
        return []
