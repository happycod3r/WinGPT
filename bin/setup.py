from customtkinter import CTkInputDialog
from wingtp_cli import WinGTPCLI
import os

class Setup:
    def __init__(self) -> None:
        self._SETUP_DONE = False
        self.wingtp_cli = WinGTPCLI()
        self.CONFIG_DIR = "./config"
        self.KEY_CONFIG_FILE = ".api_key.conf"
                    
    def createConfigDir(self, _config_dir: str) -> bool:
        if self.wingtp_cli.createDir(_config_dir) == True:
            return True
        else:
            return False
        
    def createKeyConfigFile(self, _key_file: str) -> bool:
        if self.wingtp_cli.createFile(f"{self.CONFIG_DIR}/{_key_file}") == True:
            return True
        else:
            return False
        
    def setup(self) -> bool:
        if self.createConfigDir(f"{self.CONFIG_DIR}"):
            if self.createKeyConfigFile(f"{self.KEY_CONFIG_FILE}"):
                dialog = CTkInputDialog(text="Enter your API Key\nYou can get one if needed at:\nhttps://platform.openai.com/apps: ", title="Response Count Input")
                _API_KEY = str(dialog.get_input())
                if len(_API_KEY) != 0 and _API_KEY != "None":
                    try:
                        with open(f"{self.CONFIG_DIR}/{self.KEY_CONFIG_FILE}", "w") as file:
                            if file.writable():
                                file.write(_API_KEY)
                                file.close()
                                return True
                            else:
                                return False
                    except IOError:
                        return False
                    except Exception as e:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
