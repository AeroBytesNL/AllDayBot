import logging
import os
import os.path
from env import Config
import pytz
from datetime import datetime

# Logging paths
LOG_DIR = "../logs"
LOG_NAME = "main.log"

# colors for text in terminal
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"

# Checking if log dir and files exists. If not make them
if os.path.exists(LOG_DIR) != True:
    os.mkdir(LOG_DIR)
if os.path.exists(f"{LOG_DIR}/{LOG_NAME}") != True:
    with open(f"{LOG_DIR}/{LOG_NAME}", mode='a'): pass


class Log():
    # Info logging
    def info(data):
        logger = setup_logging(logging.DEBUG)
        logger.info(str(data))
        print(f"{GREEN}INFO{RESET} - {get_time_nl()} - {data}")

    # Debug logging
    def debug(data):
        logger = setup_logging(logging.DEBUG)
        logger.debug(str(data))
        print(f"{BLUE}DEBUG{RESET} - {get_time_nl()} - {data}")

    # Warning logging
    def warning(data):
        logger = setup_logging(logging.WARNING)
        logger.warning(str(data))
        print(f"{YELLOW}WARNING{RESET} - {get_time_nl()} - {data}")

    # Error logging
    def error(data):
        logger = setup_logging(logging.ERROR)
        logger.error(str(data))
        print(f"{RED}ERROR{RESET} - {get_time_nl()} - {data}")

    # Critical logging
    def critical(data):
        logger = setup_logging(logging.CRITICAL)
        logger.critical(str(data))
        print(f"{RED}CRITICAL{RESET} - {get_time_nl()} - {data}")

# Get current Dutch data time
def get_time_nl():
    return datetime.now(pytz.timezone("Europe/Amsterdam")).strftime("%d-%m-%Y %H:%M:%S")

# Setting up logging
def setup_logging(log_level):
    logger = logging.getLogger()
    logging.basicConfig(
        filename=f"{LOG_DIR}/{LOG_NAME}",
        encoding='utf-8',
        level=log_level,
        format=f"{get_time_nl()} - %(levelname)s - %(message)s"
    )

    return logger

# Testing
# Log.info("I have started up")
# Log.debug("response time: 10ms")
# Log.warning("Oeps, things didnt go 100%")
# Log.error("Oeps, pooped my pants")
# Log.critical("FACKKKKK")