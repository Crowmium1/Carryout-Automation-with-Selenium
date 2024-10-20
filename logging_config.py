# logging_config.py
'''Logging configuration for the application.'''
import logging
import logging.config
import os
from datetime import datetime
import config

def setup_logging():
    """
    Configures the logging settings using a dictionary configuration.
    """
    # Ensure the Logs directory exists
    LOG_DIR = os.path.dirname(config.LOG_FILE)
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Define log file names with current date (optional)
    current_date = datetime.now().strftime('%Y-%m-%d')
    main_log_filename = config.LOG_FILE  # e.g., Logs/automation.log
    error_log_filename = os.path.join(LOG_DIR, f"errors_{current_date}.log")  # e.g., Logs/errors_2024-10-17.log

    # Logging configuration dictionary
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,  # Keeps the root logger enabled

        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(levelname)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'detailed': {
                'format': '[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
        },

        'handlers': {
            'console': {
                'level': 'INFO',  # Set to DEBUG to see debug messages in console
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'stream': 'ext://sys.stdout',
            },
            'file_handler': {
                'level': config.LOG_LEVEL.upper(),
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'detailed',
                'filename': main_log_filename,
                'mode': 'a',
                'maxBytes': 5 * 1024 * 1024,  # 5 MB
                'backupCount': 5,
                'encoding': 'utf-8',
            },
            'error_file_handler': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'detailed',
                'filename': error_log_filename,
                'mode': 'a',
                'maxBytes': 5 * 1024 * 1024,  # 5 MB
                'backupCount': 5,
                'encoding': 'utf-8',
            },
        },

        'loggers': {
            '': {  # Root logger
                'handlers': ['console', 'file_handler', 'error_file_handler'],
                'level': config.LOG_LEVEL.upper(),
                'propagate': True
            },
            'Code': {  # Specific logger for your project modules
                'handlers': ['console', 'file_handler', 'error_file_handler'],
                'level': config.LOG_LEVEL.upper(),
                'propagate': False
            },
            # Add more loggers here for specific modules if needed
        }
    }

    # Apply the logging configuration
    logging.config.dictConfig(LOGGING_CONFIG)

    # Initialize the project-specific logger
    logger = logging.getLogger('Code')
    logger.info("Logging is configured.")
