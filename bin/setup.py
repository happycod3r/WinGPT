from customtkinter import CTkInputDialog
from cli import WinGTPCLI
import os
from bin import persistence
class Setup:
    def __init__(self) -> None:
        self.cli = WinGTPCLI()
        self.config = persistence.Persistence()
                
        self.CONFIG_DIR = self.config.CONFIG_DIR
        self.LOGS_DIR = "./logs"
        
        self.USER_SETTINGS_FILE = self.config.USER_SETTINGS_FILE
        self.KEY_CONFIG_FILE = self.config.KEY_CONFIG_FILE
        self.USERNAME_CONFIG_FILE = self.config.USERNAME_CONFIG_FILE
        
        self.SETUP_DONE_FLAG_FILE = f"{self.CONFIG_DIR}/.setup.flag"
        
        self.USERNAME = "New user"
        self.API_KEY = None
        self.API_KEY_DIALOG_MESSAGE = "Enter your API Key\nYou can get one if needed at:\nhttps://platform.openai.com/apps"
        self.API_KEY_DIALOG_TITLE = "Enter your API key to connect & continue"
        self.USERNAME_DIALOG_MESSAGE = "Enter a user name that you want to use for authentication and display"
        self.USERNAME_DIALOG_TITLE = "Enter a username"
        
    def rollBackSetup(self) -> None:
        print("Setup failed. Rolling back changes")
        try:
            if os.path.exists(self.SETUP_DONE_FLAG_FILE):
                os.remove(self.SETUP_DONE_FLAG_FILE)
                
            if os.path.exists(self.USER_SETTINGS_FILE):
                os.remove(self.USER_SETTINGS_FILE)
            
            if os.path.exists(self.KEY_CONFIG_FILE):
                os.remove(self.KEY_CONFIG_FILE)
            
            if os.path.exists(self.USERNAME_CONFIG_FILE):
                os.remove(self.USERNAME_CONFIG_FILE)
            
            if os.path.exists(self.CONFIG_DIR):
                os.rmdir(self.CONFIG_DIR)
            
            if os.path.exists(self.LOGS_DIR):
                os.rmdir(self.LOGS_DIR) 
        except IOError as ioe:
            print(f"{ioe.__context__}")
        except Exception as e:
            print(f"{e.__context__}")            
            
    def createConfigDir(self) -> bool:
        if self.cli.createDir(self.CONFIG_DIR) == True:
            return True
        else:
            return False
        
    def createLogsDir(self) -> bool:
        if self.cli.createDir(self.LOGS_DIR) == True:
            return True
        else:
            return False
            
    def createSetupFinishedFlag(self):
        if not os.path.exists(self.SETUP_DONE_FLAG_FILE):
            if self.cli.createFile(f"{self.SETUP_DONE_FLAG_FILE}") == True:
                return True
            else:
                print("Setup failed or did not finish successfully!")
                return False
        else: 
            print("Setup failed or did not finish successfully!")
            return False
        
    def createSettingsConfigFile(self) -> bool:
        if self.cli.createFile(f"{self.USER_SETTINGS_FILE}"):
            return True
        else:
            return False
        
    def createKeyConfigFile(self) -> bool:
        if self.cli.createFile(f"{self.KEY_CONFIG_FILE}") == True:
            return True
        else:
            return False
        
    def createUsernameConfigFile(self) -> bool:
        if self.cli.createFile(f"{self.USERNAME_CONFIG_FILE}"):
            return True
        else:
            return False
        
    def setupConfig(self) -> None:
        self.config.openConfig()
        self.config.setDefaultSection("DEFAULTS")
        self.config.addSection("system")
        self.config.addOption("system", "new_user", True)
        self.config.addSection("user")
        self.config.addOption("user", "username", f"{self.USERNAME}")
        self.config.addOption("user", "api_key", f"{self.API_KEY}")
        self.config.addOption("user", "api_key_path", f"{self.KEY_CONFIG_FILE}")
        self.config.addSection("ui")
        self.config.addOption("ui", "color", "#DCE4EE")
        self.config.addOption("ui", "ui_scaling", "100%%")
        self.config.addOption("ui", "theme", "System") 
        self.config.addSection("chat")
        self.config.addOption("chat", "chat_to_file", False)
        self.config.addOption("chat", "chat_log_path", None)
        self.config.addOption("chat", "echo_chat", False)
        self.config.addOption("chat", "stream_chat", False)
        self.config.addOption("chat", "use_stop_list", False)
        self.config.addOption("chat", "chat_temperature", 1)
        self.config.addOption("chat", "chat_engine", "text-davinci-003")
        self.config.addOption("chat", "response_token_limit", 16)
        self.config.addOption("chat", "response_count", 1)
        self.config.addOption("chat", "api_base", None)
        self.config.addOption("chat", "api_type", None)
        self.config.addOption("chat", "api_version", None)
        self.config.addOption("chat", "organization", None)
        self.config.addOption("chat", "request_type", 0)
        if self.config.saveConfig():
            return True
        else: 
            return False
            
    # If any one reads this....
    # I know... I know... smh. This method is a complete mess... but it works.
    # I don't think I have ever actually nested anything this much before. 
    def setup(self) -> bool: 
        if self.createConfigDir(): # 1) Create the root config directory...
            if self.createLogsDir(): # 1) Create the logs directory...
                if self.createKeyConfigFile(): # 2) Create the file that will hold the api key... 
                    dialog = CTkInputDialog(text=f"{self.API_KEY_DIALOG_MESSAGE}", title=f"{self.API_KEY_DIALOG_TITLE}")
                    _API_KEY = str(dialog.get_input()) # 3) Get the api key from the user...
                    if len(_API_KEY) != 0 and _API_KEY != "None": # 4) Validate the api key...
                        try:
                            with open(f"{self.KEY_CONFIG_FILE}", "w") as api_key_file:
                                if api_key_file.writable():
                                    api_key_file.write(_API_KEY) # 5) Hard set the api key...
                                    api_key_file.close()
                                    self.API_KEY = _API_KEY
                                    dialog2 = CTkInputDialog(text=f"{self.USERNAME_DIALOG_MESSAGE}", title=f"{self.USERNAME_DIALOG_TITLE}")
                                    _USERNAME = str(dialog2.get_input()) # 7) Get the username from the user...
                                    if len(_USERNAME) != 0 and _USERNAME != "None": # 8) Validate the username...
                                        self.USERNAME = _USERNAME 
                                        if self.createSettingsConfigFile(): # 10) Create the main settings file.
                                            if self.createSetupFinishedFlag(): # 11) Create a flag to indicate that setup finished successfuly.
                                                if self.setupConfig(): # 12 ) Set default settings in settings.ini
                                                    return True
                                                else:
                                                    self.rollBackSetup() # 1) Roll back steps 12 - 1 if setup failed.
                                                    return False
                                            else:
                                                self.rollBackSetup() # 1) Roll back steps 11 - 1 if setup failed.
                                                return False
                                        else:
                                            self.rollBackSetup() # 1) Roll back steps 10 - 1 if setup failed.
                                            return False
                                    else:
                                        self.rollBackSetup() # 1) Roll back steps 8 - 1 if setup failed.
                                        return False
                                else:
                                    self.rollBackSetup() # 1) Roll back steps 6 - 1 if setup failed.
                                    return False
                        except FileNotFoundError:
                            self.rollBackSetup() # 1) Roll back steps 5 - 1 if setup failed.
                            return False
                        except IOError:
                            self.rollBackSetup() # 1) Roll back steps 5 - 1 if setup failed.
                            return False
                        except Exception as e:
                            print(repr(e))
                            self.rollBackSetup() # 1) Roll back steps 5 - 1 if setup failed.
                            return False
                    else:
                        self.rollBackSetup() # 1) Roll back steps 4 - 1 if setup failed.
                        return False
                else:
                    self.rollBackSetup() # 1) Roll back steps 2 - 1 if setup failed.
                    return False
            else:
                self.rollBackSetup() # 1) Roll back steps 1 - 1 if setup failed.
                return False
        else:
            self.rollBackSetup() # 1) Roll back steps 1 - 1 if setup failed.
            return False
