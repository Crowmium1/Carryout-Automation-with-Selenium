# helpers/utilities.py
'''Transfer functions'''
import logging
# import os
# from dataclasses import dataclass, asdict
# from typing import Optional, Any
import pandas as pd
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
# import config

logger = logging.getLogger(__name__)
logger.propagate = False

# This returns an object, but we are working with a mutable object, so we need to convert it to a dictionary.
# def log_error(errors_df, row_index, input_file, error_type, error_message, error_details=None):
#     """
#     Logs an error in the errors DataFrame.

#     Parameters:
#         errors_df (pd.DataFrame): The DataFrame to record errors.
#         row_index (int): The index of the row in the DataFrame where the error occurred.
#         input_file (pd.DataFrame): The original input DataFrame.
#         error_type (str): The type of error.
#         error_message (str): A detailed error message.
#         error_details (dict, optional): Additional error details.
#     Returns:
#         pd.DataFrame: The updated errors DataFrame with the new error record added.
#     """
#     # Extract common data from input_file
#     code = input_file.loc[row_index, "Code"] if "Code" in input_file.columns else None
#     product = input_file.loc[row_index, "Product"] if "Product" in input_file.columns else None
#     qty = input_file.loc[row_index, "Qty"] if "Qty" in input_file.columns else None
#     cost_per_unit = input_file.loc[row_index, "Cost per Unit"] if "Cost per Unit" in input_file.columns else None
#     total_cost = input_file.loc[row_index, "Total Cost"] if "Total Cost" in input_file.columns else None

#     # Create the error record
#     new_error = {
#         "Index": row_index,
#         "Error Type": error_type,
#         "Error Message": error_message,
#         "Code": code,
#         "Product": product,
#         "Qty": qty,
#         "Cost per Unit": cost_per_unit,
#         "Total Cost": total_cost
#     }

#     if error_details:
#         new_error.update(error_details)

#     # Append the new error to errors_df
#     new_error_df = pd.DataFrame([new_error])
#     errors_df = pd.concat([errors_df, new_error_df], ignore_index=True)
#     logger.info("Error logged: %s", new_error)

#     # Append the new_error as a new row
#     errors_df.loc[len(errors_df)] = new_error
#     logger.info("Error logged: %s", new_error)

#     return errors_df

def log_error(errors_df, row_index, input_file, error_type, error_message, error_details=None):
    """
    Logs an error in the errors DataFrame.
    Parameters:
        errors_df (pd.DataFrame): The DataFrame to record errors.
        row_index (int): The index of the row in the DataFrame where the error occurred.
        input_file (pd.DataFrame): The original input DataFrame.
        error_type (str): The type of error.
        error_message (str): A detailed error message.
        error_details (dict, optional): Additional error details.
    Returns:
        None
    """
    # Extract common data from input_file
    code = input_file.loc[row_index, "Code"] if "Code" in input_file.columns else None
    product = input_file.loc[row_index, "Product"] if "Product" in input_file.columns else None
    qty = input_file.loc[row_index, "Qty"] if "Qty" in input_file.columns else None
    cost_per_unit = input_file.loc[row_index, "Cost per Unit"] if "Cost per Unit" in input_file.columns else None
    total_cost = input_file.loc[row_index, "Total Cost"] if "Total Cost" in input_file.columns else None

    new_error = {
        "Index": row_index,
        "Error Type": error_type,
        "Error Message": error_message,
        "Code": code,
        "Product": product,
        "Qty": qty,
        "Cost per Unit": cost_per_unit,
        "Total Cost": total_cost
    }

    if error_details:
        new_error.update(error_details)

    # Append the new error to errors_df
    errors_df.loc[len(errors_df)] = new_error
    logger.info("Error logged: %s", new_error)

# This uses openpyxl to append the errors_df to the existing Excel file instead of xlsx writer.
def save_errors(errors_df, filepath, batch_num):
    """
    Saves the errors DataFrame to a new sheet in the Excel file.
    """
    try:
        print(f"Saving errors to: {filepath}")
        errors_sheet_name = f'Errors Batch {batch_num + 1}'
        if not errors_df.empty:
            # Append the errors_df to the existing Excel file
            with pd.ExcelWriter(filepath, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                errors_df.to_excel(writer, sheet_name=errors_sheet_name, index=False)
            logger.info("Errors DataFrame saved to '%s' successfully.", filepath)
        else:
            print(f"No errors to save for batch {batch_num + 1}")

    except Exception as e:
        logger.error("Failed to save the Errors DataFrame to an Excel file: %s", e, exc_info=True)

# def save_errors(errors_df, filepath, input_file):
#     """
#     Saves the input DataFrame and errors DataFrame to separate sheets in an Excel file.
#     """
#     try:
#         print(f"Saving errors to: {filepath}")
#         # Ensure the directory exists
#         os.makedirs(os.path.dirname(filepath), exist_ok=True)
#         with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
#             input_file.to_excel(writer, sheet_name='Input Data', index=False)
#             errors_df.to_excel(writer, sheet_name='Errors', index=False)
#         logger.info("DataFrames saved to '%s' successfully.", filepath)
#     except Exception as e:
#         logger.error("Failed to save the DataFrames to an Excel file: %s", e, exc_info=True)

# @dataclass
# class ErrorRecord:
#     '''Class to represent an error record.'''
#     Index: Optional[int]
#     Error_Type: str
#     Error_Message: str
#     Code: Optional[str] = None
#     Product: Optional[str] = None
#     Qty: Optional[Any] = None
#     Cost_per_Unit: Optional[Any] = None
#     Total_Cost: Optional[Any] = None
#     Difference: Optional[Any] = None
#     Additional_Data: Optional[str] = None

# def log_error_dataclass(errors_df, error_record: ErrorRecord):
#     """
#     Logs an error in the errors DataFrame.

#     Parameters:
#         errors_df (pd.DataFrame): The DataFrame to record errors.
#         error_record (ErrorRecord): An instance of ErrorRecord containing error details.

#     Returns:
#         pd.DataFrame: The updated errors DataFrame with the new error record added.
#     """
#     # Convert the data class to a dictionary
#     error_dict = asdict(error_record)

#     # Create a DataFrame from the error_dict
#     new_error_df = pd.DataFrame([error_dict])

#     # Concatenate the new_error_df to errors_df
#     errors_df = pd.concat([errors_df, new_error_df], ignore_index=True)

#     return errors_df
