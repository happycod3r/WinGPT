from wingtp_cli import WinGTPCLI
from bin import setup
import customtkinter as ctk
import subprocess
import os

class Initialize:
    def __init__(self) -> None:
        self._setup = setup.Setup()
        self.WGTP_GUI_V010 = "wingtp_gui.py"
        self.USAGE_STATES = ["unused", "used"]
        self.USAGE_STATE = self.USAGE_STATES[0]
        self.cli = WinGTPCLI()
            
        self.key_file_path = f"{self._setup.CONFIG_DIR}/{self._setup.KEY_CONFIG_FILE}"     
        if os.path.exists(self.key_file_path):
            try:
                with open(self.key_file_path, "r") as file:
                    key = file.read()
                    file.close()
            except IOError:
                return False
            except Exception as e:
                return False
            if len(key) == 0 or key == "None":
                if self._setup.setup() == True:
                    self.runWinGTPGUI()    
                else:
                    print("Setup failed!")
                    exit(1)
            else:
                self.runWinGTPGUI()
        else:
            if self._setup.setup() == True:
                self.runWinGTPGUI()    
            else:
                print("Setup failed!")
                exit(1)    
        
         
        
    def runWinGTPGUI(self) -> None:
        subprocess.run(["python", f"{self.WGTP_GUI_V010}"])

def wingtp_gui_init() -> None:
    init = Initialize()

wingtp_gui_init()
