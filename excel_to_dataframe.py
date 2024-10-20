'''This script will take an excel file and convert it to a pandas dataframe.'''
import logging
import pandas as pd
import config
from logging_config import setup_logging

# Set pandas display options for better alignment and readability
pd.set_option('display.float_format', lambda x: f"{x:,.2f}")  # Format floats to 2 decimal places
pd.set_option('display.max_columns', None)   # Display all columns
pd.set_option('display.width', 1000)         # Set display width to prevent wrapping

def clean_columns(df, columns):
    """
    Clean currency columns by removing non-numeric characters and converting to float.
    """
    for column in columns:
        if column in df.columns:
            try:
                df[column] = df[column].astype(str).str.replace(r'[^\d.]', '', regex=True).replace('', '0').astype(float)
                df[column] = df[column].replace({'¤': '', '£': '', '$': ''}, regex=True)
                
            except Exception as e:
                print(f"Error cleaning column '{column}': {e}")
        else:
            print(f"Warning: Column '{column}' not found in DataFrame.")
    return df

# Paths
quantity_path = config.INPUT_QUANTITY_PATH
product_path = config.INPUT_TIME_PATH

# Load the CSV files
quantity_df = pd.read_csv(quantity_path)
product_df = pd.read_csv(product_path)

# List headers
# quantity_df_headings = quantity_df.columns.tolist()
# product_df_headings = product_df.columns.tolist()

# Columns to Drop
columns_to_drop_quantity = ['Unnamed: 0', 'Unnamed: 4', 'Unnamed: 6', 'Unnamed: 7',
                            'Unnamed: 8', 'Unnamed: 10']
columns_to_drop_product = ['Unnamed: 0', 'Order Qty\n(Pack / Case)','Unnamed: 3',
                           'Unnamed: 5', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 10']

# Drop specified columns
quantity_df = quantity_df.drop(columns_to_drop_quantity, axis=1, errors='ignore')
product_df = product_df.drop(columns_to_drop_product, axis=1, errors='ignore')

# Rename columns
quantity_df = quantity_df.rename(columns={'Description': 'Product', 'Cost per Unit': 
                                          'Cost per Unit', 'Total': 'Total Cost'})
product_df = product_df.rename(columns={'Description': 'Product', 'Order Size': 'Unit',
                                        'Price': 'Cost per Unit'})

# Strip whitespace from column names
quantity_df.columns = quantity_df.columns.str.strip()
product_df.columns = product_df.columns.str.strip()

# Clean columns
clean_columns(quantity_df, ['Cost per Unit', 'Total Cost'])
clean_columns(product_df, ['Cost per Unit'])

# Filter rows where 'Code' contains only digits
product_df['Code'] = product_df['Code'].astype(str).str.strip()
is_numeric = product_df['Code'].str.isdigit()
non_numeric_count = (~is_numeric).sum()
if non_numeric_count > 0:
    product_df = product_df.loc[is_numeric].copy()
# print(f"Removed {non_numeric_count} rows with non-numeric 'Code' values.")
# print(non_numeric_count)
# print(is_numeric)

quantity_df['Product'] = quantity_df['Product'].astype(str).str.strip().str.replace(r'\s+', ' ', regex=True)
product_df['Product'] = product_df['Product'].astype(str).str.strip().str.replace(r'\s+', ' ', regex=True)

# # Print heads and shapes
# print("\n--- Quantity DataFrame Head ---")
# print(quantity_df.head())
# print("\n--- Product DataFrame Head ---")
# print(product_df.head())
# print("\n--- Quantity DataFrame Shape:", quantity_df.shape)
# print("--- Product DataFrame Shape:", product_df.shape)

# Proceed with merging
merged_df = pd.merge(quantity_df, product_df[['Code', 'Product']], on='Product', how='left')
print("Merged DataFrames on 'Product'.")

# Identify and count missing 'Code' entries
missing_code = merged_df['Code'].isna().sum()
if missing_code > 0:
    print(f"{missing_code} rows have unmatched 'Product' and missing 'Code'. These will be dropped.")
    merged_df = merged_df.dropna(subset=['Code']).copy()
print(f"Merged DataFrame shape after dropping unmatched 'Code': {merged_df.shape}")

# Reorder columns
desired_order = ['Code', 'Product', 'Unit', 'Qty', 'Cost per Unit', 'Total Cost']
merged_df = merged_df[desired_order]
print("Reordered columns to desired order.")

# Identify duplicates based on 'Description' and create Dataframe
duplicates_mask = merged_df.duplicated(subset=['Product'], keep='first')
duplicates_df = merged_df.loc[duplicates_mask].copy()

# Keep only unique rows
unique_df = merged_df.loc[~duplicates_mask].copy()

# Reset index for both DataFrames
unique_df.reset_index(drop=True, inplace=True)
duplicates_df.reset_index(drop=True, inplace=True)

# # Save the DataFrames to CSV files
# print(f"Unique DataFrame shape: {unique_df.shape}")
# print("\n--- Unique DataFrame Head ---")
# print(unique_df.head())
# print("\n--- Unique DataFrame Head ---")
# print(unique_df.head())
# unique_df.to_csv('unique_output.csv', index=False)
# print("Unique DataFrame saved to 'unique_output.csv'.")

# # Duplicates DataFrame
# print(f"Duplicates DataFrame shape: {duplicates_df.shape}")
# print("\n--- Duplicates DataFrame Head ---")
# print(duplicates_df.head())
# duplicates_df.to_csv('duplicates_output.csv', index=False)
# print("Duplicates DataFrame saved to 'duplicates_output.csv'.")
# # Check if 'Code' column contains non-numeric characters
# unique_non_numerics = unique_df[unique_df['Code'].astype(str).str.contains(r'\D', regex=True)]
# duplicates_non_numerics = duplicates_df[duplicates_df['Code'].astype(str).str.contains(r'\D', regex=True)]
# print(f"Unique DataFrame Weird Characters: {unique_non_numerics}")
# print(f"Duplicates DataFrame Weird Characters: {duplicates_non_numerics}")