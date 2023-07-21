import os.path

class Globals:
    def __init__(self):
        self.CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
        self.LOGS_DIR = f"{self.CURRENT_PATH}/logs"
        self.
