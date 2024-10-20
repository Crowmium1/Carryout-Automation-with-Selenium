# Code/main.py
'''Main script to execute the Selenium automation workflow.'''
import traceback
import os
import sys
import logging
import math
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from excel_to_dataframe import unique_df
from config import CHECKPOINT_PATH, OUTPUT_XLSX_PATH
from logging_config import setup_logging
from helpers import (
    initialize_driver,
    login_sequence,
    click_got_it_button,
    select_business,
    select_delivery,
    select_carryout,
    set_up,
    save_errors,
    extract_all_cells,
    fill_fields,
    close_form,
    get_total_costs,
    log_error,
    save_form
)
setup_logging()
logger = logging.getLogger(__name__)

def loop(driver, input_file, data_row_index, errors_df):
    '''Loops through the DataFrame and processes each row.'''
    try:
        search_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "web-md-button-189fl7lckkbbqvmi")))
        driver.execute_script("arguments[0].scrollIntoView(true);", search_button)
        driver.execute_script("document.querySelectorAll('.md-scroll-mask').forEach(e => e.remove());")
        driver.execute_script("arguments[0].click();", search_button)
        search_textbox = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "web-input-189fl7nukkbbymu9")))
        search_textbox.clear()
        product_code = str(input_file.loc[data_row_index, "Code"]).strip()
        product_description = str(input_file.loc[data_row_index, "Product"]).strip()
        search_textbox.send_keys(product_code)
        all_cell_data = extract_all_cells(driver, table_xpath=".//table[contains(@id, 'web-table')]", timeout=30)
        
        # Check if the product is found in the web table
        matching_row = None
        for row_data in all_cell_data:
            if (row_data.get('Product Code') == product_code and
                    row_data.get('Product') == product_description):
                matching_row = row_data
                break
        if matching_row is None:
            error_message = f"Product code {product_code} with description '{product_description}' not found in the web table."
            error_details = {'Code': product_code, 'Product': product_description}
            log_error(
                errors_df,
                row_index=data_row_index,
                input_file=input_file,
                error_type="Product Not Found",
                error_message=error_message,
                error_details=error_details
            )
            print(error_message)
            close_form(driver)
            return
        fill_data = input_file.loc[data_row_index]
        fill_fields(driver, fill_data)
        total_cost_df, total_cost_web = get_total_costs(driver, input_file, data_row_index)
        difference = total_cost_web - total_cost_df
        print(f"Total Cost DF: {total_cost_df}")
        print(f"Total Cost Web: {total_cost_web}")
        print(f"The difference between total costs is: {difference}")
        if not math.isclose(total_cost_df, total_cost_web, rel_tol=1e-4):
            error_message = "Expected total cost does not match web total cost."
            error_details = {
                'Qty': float(fill_data["Qty"]),
                'Cost per Unit': float(fill_data["Cost per Unit"]),
                'Total Cost': float(fill_data["Total Cost"]),
                'Web_Difference': difference
            }
            log_error(
                errors_df,
                row_index=data_row_index,
                input_file=input_file,
                error_type="Total Cost Mismatch",
                error_message=error_message,
                error_details=error_details
            )
            print(f"Error logged: {error_message}")
            close_form(driver)
            return
        print(f"The totals match for DataFrame row: '{data_row_index + 1}'")
        close_form(driver)
    except Exception as e:
        traceback.print_exc()
        logger.error("An error occurred at row %s: %s", data_row_index, str(e))
        error_message = str(e)
        traceback_str = traceback.format_exc()
        log_error(
            errors_df,
            row_index=data_row_index,
            input_file=input_file,
            error_type="Processing Error",
            error_message=error_message,
            error_details={'Traceback': traceback_str}
        )
        close_form(driver)
        return

def main(file, reset_checkpoint=False):
    """
    Main function to execute the Selenium automation workflow.
    Processes the DataFrame in batches, with checkpointing.
    """
    if reset_checkpoint and os.path.exists(CHECKPOINT_PATH):
        os.remove(CHECKPOINT_PATH)
        print("Checkpoint has been reset. Starting from the first batch.")
    driver = initialize_driver()
    logger.info("Application started.")

    try:
        if os.path.exists(CHECKPOINT_PATH):
            with open(CHECKPOINT_PATH, 'r', encoding="utf-8") as f:
                checkpoint_data = f.read().strip()
                if checkpoint_data.isdigit():
                    last_processed_batch_num = int(checkpoint_data)
                    print(f"Resuming from batch number {last_processed_batch_num}")
                else:
                    last_processed_batch_num = 0
        else:
            last_processed_batch_num = 0

        login_sequence(driver)
        click_got_it_button(driver)
        select_business(driver)
        select_delivery(driver)
        select_carryout(driver)
        set_up(driver)
        batch_size = 50
        total_rows = file.shape[0]
        num_batches = (total_rows + batch_size - 1) // batch_size
        output_filepath = OUTPUT_XLSX_PATH
        # At the start, write the 'Input Data' sheet to the Excel file if starting fresh
        if last_processed_batch_num == 0:
            os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
            with pd.ExcelWriter(output_filepath, engine='openpyxl') as writer:
                file.to_excel(writer, sheet_name='Input Data', index=False)
            print(f"Input data saved to {output_filepath}")

        for batch_num in range(last_processed_batch_num, num_batches):
            start_index = batch_num * batch_size
            end_index = min(start_index + batch_size, total_rows)
            batch_df = file.iloc[start_index:end_index].reset_index(drop=True)
            errors_df = pd.DataFrame(columns=[
                'Index', 'Error Type', 'Error Message',
                'Code', 'Product', 'Qty', 'Cost per Unit',
                'Total Cost', 'Web_Difference'])

            for index in batch_df.index:
                data_row_index = start_index + index
                try:
                    loop(driver, file, data_row_index, errors_df)
                    print(f"Processed {data_row_index + 1} out of {total_rows} successfully.")
                except Exception as e:
                    error_message = str(e)
                    traceback_str = traceback.format_exc()
                    log_error(
                        errors_df,
                        row_index=data_row_index,
                        input_file=file,
                        error_type="Processing Error",
                        error_message=error_message,
                        error_details={'Traceback': traceback_str}
                    )
                    continue

            save_errors(errors_df, output_filepath, batch_num)
            print(f"Batch {batch_num + 1} completed. Errors saved to {output_filepath}")
            with open(CHECKPOINT_PATH, 'w', encoding='utf-8') as f:
                f.write(str(batch_num + 1))  # Next batch to process
    except Exception as e:
        logger.error("An error occurred: %s", str(e), exc_info=True)
    finally:
        print("End of script.")
        save_form(driver)
        # driver.quit()

if __name__ == "__main__":
    reset = '--reset' in sys.argv
    main(unique_df, reset_checkpoint=reset)
    if os.path.exists(CHECKPOINT_PATH):
        os.remove(CHECKPOINT_PATH)
