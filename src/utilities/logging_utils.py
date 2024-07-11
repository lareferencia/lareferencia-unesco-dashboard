import logging
from logging.handlers import RotatingFileHandler
import os
import time
from functools import wraps

# Configuration
log_directory = os.path.join(os.path.dirname(__file__), '..', 'logs')
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Set up the log file path, maximum log size, and number of backup files
log_file_path = os.path.join(log_directory, 'app_performance.log')
max_log_size = 1 * 1024 * 1024  # 1 MB
backup_count = 3  # Number of backup files to keep

# Set up a rotating file handler
rotating_handler = RotatingFileHandler(log_file_path, maxBytes=max_log_size, backupCount=backup_count)
rotating_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - Execution Time: %(message)s'))

# Configure the root logger to use the rotating file handler
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(rotating_handler)
# Define a decorator for timing functions
def log_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logging.info(f'{func.__name__} executed in {execution_time} seconds')
        return result
    return wrapper

# Example of applying the decorator
@log_execution_time
def some_function_to_time():
    # Function logic here
    pass
