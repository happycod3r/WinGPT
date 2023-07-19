from cli import WinGTPCLI
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
                self.runWinGTPGUI(False, f"{self.userName()}")
        else:
            if self._setup.setup() == True:
                self.runWinGTPGUI(True, str(self._setup.USERNAME))    
            else:
                print("Setup failed!")
                exit(1)
    
    def userName(self) -> str:
        return self.cli.readFromFile(self._setup.USERNAME_CONFIG_FILE)
    
    def runWinGTPGUI(self, new_user: bool = True, username: str = "new guy") -> None:
        user_info = {
            "status": new_user,
            "name": username,
        }
        subprocess.run(["python", self.WGTP_GUI_V010, str(user_info["status"]), user_info["name"]])
    
def wingtp_gui_init() -> None:
    init = Initialize()

wingtp_gui_init()
