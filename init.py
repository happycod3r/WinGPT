from bin import setup
import subprocess
import os

class Initialize:
    def __init__(self) -> None:
        self._setup = setup.Setup()
        self.WGTP_GUI_V010 = "wingtp_gui.py"
         
        if not os.path.exists(self._setup.SETUP_DONE_FLAG_FILE):
            if self._setup.setup() == True:
                self.runWinGTPGUI(True)    
            else:
                print("Setup failed!")
                exit(1)
        else:
            self.runWinGTPGUI(False)    
    
    def runWinGTPGUI(self, new_user: bool = True) -> None:
        subprocess.run(["python", self.WGTP_GUI_V010])
    
def wingtp_gui_init() -> None:
    init = Initialize()

wingtp_gui_init()
