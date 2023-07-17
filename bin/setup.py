from customtkinter import CTkInputDialog
from wingtp_cli import WinGTPCLI
import os

class Setup:
    def __init__(self) -> None:
        self.wingtp_cli = WinGTPCLI()
        self.CONFIG_DIR = "./config"
        self.KEY_CONFIG_FILE = "./config/.api_key.conf"
        self.SETUP_DONE_FLAG_FILE = "./config/.setup.flag"
        self.USER_SETTINGS_FILE = "./config/settings.conf"
        self.API_KEY_DIALOG_MESSAGE = "Enter your API Key\nYou can get one if needed at:\nhttps://platform.openai.com/apps"
        self.API_KEY_DIALOG_TITLE = "Enter your API key to connect & continue"
        self.USERNAME_CONFIG_FILE = "./config/.user.conf"
        self.USERNAME = "New user"
        self.USERNAME_DIALOG_MESSAGE = "Enter a user name that you want to use for authentication and display"
        self.USERNAME_DIALOG_TITLE = "Enter a username"
        
    def rollBackSetup(self) -> None:
        print("Setup failed. Rolling back changes")
        try:
            
            if os.path.exists(self.USER_SETTINGS_FILE):
                os.remove(self.USER_SETTINGS_FILE)
        
            if os.path.exists(self.SETUP_DONE_FLAG_FILE):
                os.remove(self.SETUP_DONE_FLAG_FILE)
            
            if os.path.exists(self.KEY_CONFIG_FILE):
                os.remove(self.KEY_CONFIG_FILE)
            
            if os.path.exists(self.CONFIG_DIR):
                os.rmdir(self.CONFIG_DIR)
        except IOError as ioe:
            print(f"{ioe.__context__}")
        except Exception as e:
            print(f"{e.__context__}")            
            
    def createSetupFinishedFlag(self):
        if not os.path.exists(self.SETUP_DONE_FLAG_FILE):
            if self.wingtp_cli.createFile(f"{self.SETUP_DONE_FLAG_FILE}") == True:
                return True
            else:
                print("Setup failed or did not finish successfully!")
                return False
        else: 
            print("Setup failed or did not finish successfully!")
            return False
                    
    def createConfigDir(self) -> bool:
        if self.wingtp_cli.createDir(self.CONFIG_DIR) == True:
            return True
        else:
            return False
        
    def createKeyConfigFile(self) -> bool:
        if self.wingtp_cli.createFile(f"{self.KEY_CONFIG_FILE}") == True:
            return True
        else:
            return False
        
    def createUsernameConfigFile(self) -> bool:
        if self.wingtp_cli.createFile(f"{self.USERNAME_CONFIG_FILE}"):
            return True
        else:
            return False
            
    def setup(self) -> bool:
        # The following 5 steps are critical to the normal function of WinGTP. 
        # If any of these steps fail then setup must fail otherwise the user 
        # gets a broken program. Only after these steps succeed will the api key 
        # be hard set and the gui be loaded for use. Aside from theme/color settings 
        # all of wgtps functionality relies on the openai api being successfully 
        # loaded with a valid api key so there is really no point in showing the 
        # gui if setup fails. 
        if self.createConfigDir(): # 1) Create the root config directory...
            if self.createKeyConfigFile(): # 2) Create the file that will hold the api key... 
                dialog = CTkInputDialog(text=f"{self.API_KEY_DIALOG_MESSAGE}", title=f"{self.API_KEY_DIALOG_TITLE}")
                _API_KEY = str(dialog.get_input()) # 3) Get the api key from the user...
                if len(_API_KEY) != 0 and _API_KEY != "None": # 4) Validate the api key...
                    try:
                        with open(f"{self.KEY_CONFIG_FILE}", "w") as api_key_file:
                            if api_key_file.writable():
                                api_key_file.write(_API_KEY) # 5) Hard set the api key...
                                api_key_file.close()
                                if self.createUsernameConfigFile(): # 6) Create the username config file...
                                    #/////////////////////////////// 
                                    dialog2 = CTkInputDialog(text=f"{self.USERNAME_DIALOG_MESSAGE}", title=f"{self.USERNAME_DIALOG_TITLE}")
                                    _USERNAME = str(dialog2.get_input()) # 7) Get the username from the user...
                                    if len(_USERNAME) != 0 and _USERNAME != "None":
                                        self.USERNAME = _USERNAME 
                                        try:
                                            with open(f"{self.USERNAME_CONFIG_FILE}", "w") as username_file:
                                                if username_file.writable():
                                                    username_file.write(f"{self.USERNAME}") # 8) Hard set the username...
                                                    username_file.close()
                                                else:
                                                    return False
                                        except IOError:
                                            return False
                                        except Exception as e:
                                            print(f"{e.__context__}")
                                            return False
                                        if self.createSetupFinishedFlag(): # 9) Create a flag to indicate that setup finished.
                                            return True
                                        else:
                                            self.rollBackSetup() # 10) Roll back step 9 - 1, Hopefully noone reaces this point.
                                            return False
                                    else:
                                        return False
                                    #////////////////////////////////
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
