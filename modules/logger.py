import paths
import logging
import os

class LogManager:
    def __init__(self) -> None:
        self.CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
        self.LOGS_DIR = f"{paths.LOGS_DIR}"
        self.SYSTEM_LOG_FILE = f"{paths.SYSTEM_LOG_FILE}"
        
        logging.basicConfig(
            filename = f"{self.SYSTEM_LOG_FILE}",
            level = logging.DEBUG
        )
        
        self.logger = logging.getLogger()

        
