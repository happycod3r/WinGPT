import logging
import os

class LogManager:
    def __init__(self) -> None:
        self.CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
        self.LOGS_DIR = f"{self.CURRENT_PATH}\\..\\logs"
        self.SYSTEM_LOG_FILE = f"{self.LOGS_DIR}\\system.log"
        
        logging.basicConfig(
            filename = f"{self.SYSTEM_LOG_FILE}",
            level = logging.DEBUG
        )
        
        self.logger = logging.getLogger()

        