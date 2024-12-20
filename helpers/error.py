import logging
import os
import os.path
from env import Config
import pytz
from datetime import datetime

# Logging paths
LOG_DIR = rf"{os.getcwd()}/logs"
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
# If write permissions are missing
if os.access(f"{LOG_DIR}/{LOG_NAME}", os.W_OK) != True:
    print(f"{RED}ERROR{RESET} - Geen schrijfpermissies voor {log_path}")

class Log():
    # Info
    @staticmethod
    def info(data):
        logger = setup_logging(logging.DEBUG)
        print(f"{GREEN}INFO{RESET} - {get_time_nl()} - {data}")

        if Config.DEBUG != True: return
        logger.info(str(data))

    # Debug
    @staticmethod
    def debug(data):
        if Config.DEBUG != True: return

        logger = setup_logging(logging.DEBUG)
        logger.debug(str(data))
        print(f"{BLUE}DEBUG{RESET} - {get_time_nl()} - {data}")

    # Warning
    @staticmethod
    def warning(data):
        logger = setup_logging(logging.WARNING)
        logger.warning(str(data))
        print(f"{YELLOW}WARNING{RESET} - {get_time_nl()} - {data}")

    # Error
    @staticmethod
    def error(data):
        logger = setup_logging(logging.ERROR)
        logger.error(str(data))
        print(f"{RED}ERROR{RESET} - {get_time_nl()} - {data}")

# Get current Dutch data time
def get_time_nl():
    return datetime.now(pytz.timezone("Europe/Amsterdam")).strftime("%d-%m-%Y %H:%M:%S")

def initialize_logger():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    log_file_path = os.path.join(LOG_DIR, LOG_NAME)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file_path, encoding="utf-8"),
            logging.StreamHandler()  # Log ook naar console
        ],
    )

# Setting up logging
def setup_logging(log_level):
    try:
        logger = logging.getLogger("auticodes_logging")

        if not logger.handlers:
            logger.setLevel(log_level)

            file_handler = logging.FileHandler(f"{LOG_DIR}/{LOG_NAME}", encoding='utf-8')
            file_handler.setLevel(log_level)
            formatter = logging.Formatter(f"{get_time_nl()} - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            print(f"{GREEN}INFO{RESET} - Logging naar bestand ingesteld op {LOG_DIR}/{LOG_NAME}")

        return logger
    except Exception as error:
        print(f"{RED}ERROR{RESET} - {get_time_nl()} - {error}")
        raise