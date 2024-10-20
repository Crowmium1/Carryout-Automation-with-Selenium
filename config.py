# config.py
import os
import configparser

# Initialize the parser
config = configparser.ConfigParser()

# Define the path to the config.ini file
CONFIG_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')

# Read the config.ini file
config.read(CONFIG_FILE_PATH)

# Base directory (Code/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Access configurations
# Webdriver details
DRIVER_PATH = os.path.join(BASE_DIR, config.get('webdriver_details', 'driver_path'))
BROWSER = config.get('webdriver_details', 'browser')

# Login details
URL = config.get('login_details', 'url')
COMPANY_CODE = config.get('login_details', 'company_code')
USERNAME = config.get('login_details', 'username')
PASSWORD = config.get('login_details', 'password')

# Order details
BUSINESS_NAME = config.get('order_details', 'business_name')
SUPPLIER_NAME = config.get('order_details', 'supplier_name')
DELIVERY_DATE = config.get('order_details', 'delivery_date')
REFERENCE_NUMBERS = config.get('order_details', 'reference_numbers')

# Input paths
INPUT_QUANTITY_PATH = os.path.join(BASE_DIR, config.get('input_paths', 'INPUT_QUANTITY_PATH'))
INPUT_TIME_PATH = os.path.join(BASE_DIR, config.get('input_paths', 'INPUT_TIME_PATH'))
DOCKET_CSV_PATH = os.path.join(BASE_DIR, config.get('input_paths', 'DOCKET_CSV_PATH'))
DOCKET_PICKLE_PATH = os.path.join(BASE_DIR, config.get('input_paths', 'DOCKET_PICKLE_PATH'))

# Output paths
OUTPUT_CSV_PATH = os.path.join(BASE_DIR, config.get('output_paths', 'OUTPUT_CSV_PATH'))
OUTPUT_XLSX_PATH = os.path.join(BASE_DIR, config.get('output_paths', 'OUTPUT_XLSX_PATH'))
CHECKPOINT_PATH = os.path.join(BASE_DIR, config.get('output_paths', 'CHECKPOINT_PATH'))
ERRORS_PATH = os.path.join(BASE_DIR, config.get('output_paths', 'ERRORS_PATH'))

# Logging configurations
LOG_FILE = os.path.join(BASE_DIR, config.get('logging', 'log_file'))
LOG_LEVEL = config.get('logging', 'log_level')
