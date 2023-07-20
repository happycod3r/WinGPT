import setup
import setuptools
import subprocess
import os

class Initialize:
    def __init__(self) -> None:
    
         
        if not os.path.exists(self._setup.SETUP_DONE_FLAG_FILE):
            pass
        else:
            self.runWinGTPGUI(False)    
    
    def runWinGTPGUI(self, new_user: bool = True) -> None:
        pass
    
def wingtp_init() -> None:
    init = Initialize()

wingtp_init()
