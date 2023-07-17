from wingtp_cli import WinGTPCLI
from bin import setup
import customtkinter as ctk
import subprocess
import os

class Initialize:
    def __init__(self) -> None:
        self._setup = setup.Setup()
        self.WGTP_GUI_V010 = "wingtp_gui.py"
        self.cli = WinGTPCLI()
        self.NEW_USER = True
        self.USERNAME = None
            
        self.key_file_path = f"{self._setup.KEY_CONFIG_FILE}"     
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
                    self.runWinGTPGUI(True, str(self._setup.USERNAME))    
                else:
                    print("Setup failed!")
                    exit(1)
            else:
                # !!! FOR THE MORNING YOU LEFT OFF HERE !!!
                # - All calls to runWinGTPGUI(True) or runWinGTPGUI(False) needs to make a call to 
                # a getUsername() function as the second parameter so that both new_user and username 
                # get passed to the gui. I didn't look but I think cli still has one I can just 
                # modify as it's not being used yet anywhere.
                #
                _username = self.cli.readFromFile(self._setup.USERNAME_CONFIG_FILE)
                self.runWinGTPGUI(False, _username)
        else:
            if self._setup.setup() == True:
                self.runWinGTPGUI(True, str(self._setup.USERNAME))    
            else:
                print("Setup failed!")
                exit(1)
                
    def runWinGTPGUI(self, new_user: bool, username: str = "new guy") -> None:
        subprocess.run(["python", self.WGTP_GUI_V010, str(new_user), username])
    
def wingtp_gui_init() -> None:
    init = Initialize()

wingtp_gui_init()
