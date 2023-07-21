import customtkinter
import persistence
from PIL import Image
from ctrls import ctkframe
import os
import gui

customtkinter.set_appearance_mode("dark")

class Setup(customtkinter.CTk):
    width = 900
    height = 600

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.config = persistence.Persistence()
        
        self.CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
        self.CONFIG_DIR = f"{self.CURRENT_PATH}\\config"
        self.LOGS_DIR = f"{self.CURRENT_PATH}\\logs"
        self.USER_SETTINGS_FILE = f"{self.CONFIG_DIR}\\settings.ini"
        self.KEY_CONFIG_FILE = f"{self.CONFIG_DIR}\\.api_key.ini"
        self.SETUP_DONE_FLAG_FILE = f"{self.CONFIG_DIR}\\.setup.flag"
        
        self.USERNAME = None
        self.API_KEY = None
        
        #//////////// SETUP ////////////
        if not self.setup():
            self.setupFailedEvent()
        
        #///////////////////////////////
        
        #//////////// SETUP FORM ////////////
        self.title("Wingtp & OpenAI Setup")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        # load and create background image
    
        self.bg_image = customtkinter.CTkImage(Image.open(self.CURRENT_PATH + "\\images\\openai_dark.png"), size=(self.width, self.height))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        self.setup_frame = ctkframe.CustomTkFrame(self)
        self.setup_frame.grid(row=0, column=0, sticky="ns")
        
        self.setup_label = customtkinter.CTkLabel(self.setup_frame, text="WinGTP Setup", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.setup_label.grid(row=0, column=0, padx=30, pady=(150, 15))
        
        self.username_entry = customtkinter.CTkEntry(self.setup_frame, width=200, placeholder_text="username")
        self.username_entry.grid(row=1, column=0, padx=30, pady=(15, 15))
        
        self.api_key_entry = customtkinter.CTkEntry(self.setup_frame, width=200, placeholder_text="api key")
        self.api_key_entry.grid(row=2, column=0, padx=30, pady=(0, 15))
        
        self.setup_done_button = customtkinter.CTkButton(self.setup_frame, text="Finish Setup", command=self.formDoneEvent, width=200)
        self.setup_done_button.grid(row=3, column=0, padx=30, pady=(15, 15))

    def createDir(self, path: str) -> bool:
        if not os.path.exists(path):
            try:
                os.mkdir(path)
                return True
            except FileNotFoundError:
                print("FileNotFoundError: File not found error")
                return False
            except IOError:
                print("IOError: Could not create directory.")
            except Exception as e:
                print(repr(e))
                return False
        return True

    def createFile(self, file_path: str) -> bool:
        if not os.path.exists(file_path):
            try:
                with open(file_path, 'w') as file:
                    return True
            except FileNotFoundError:
                print(f"File '{file_path}' already exists!")
                return False
            except IOError:
                return False
            except Exception as e:
                print(repr(e))
                return False
        return True

    def createSetupDoneFlagFile(self) -> bool:
        if not self.createFile(self.SETUP_DONE_FLAG_FILE):
            return False
        else:
            return True

    def setupConfig(self) -> None:
        self.config.openConfig()
        self.config.setDefaultSection("DEFAULTS")
        self.config.addSection("system")
        self.config.addOption("system", "new_user", True)
        self.config.addOption("system", "config_dir", f"{self.CURRENT_PATH}/config")
        self.config.addOption("system", "logs_dir", f"{self.CURRENT_PATH}/logs") 
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

    def createConfigFiles(self) -> bool:
        if not self.createDir(self.CONFIG_DIR):
            return False
        elif not self.createDir(self.LOGS_DIR):
            return False
        elif not self.createFile(self.USER_SETTINGS_FILE):
            return False
        elif not self.createFile(self.KEY_CONFIG_FILE):
            return False
        else:
            return True

    def validateAPIKey(self, api_key: str) -> bool:
        if not (api_key.startswith('sk-') and len(api_key) == 51):
            return False
        else:
            return True

    def writeAPIKey(self, api_key: str) -> bool:
        try:
            with open(self.KEY_CONFIG_FILE, "w") as keyfile:
                keyfile.write(api_key)
                keyfile.close()
                return True
        except FileNotFoundError:
            return False
        except IOError:
            return False
        except Exception as e:
            print(repr(e))
            return False
        
    def rollBackSetup(self) -> None:
        print("Setup failed. Rolling back changes")
        try:
            if os.path.exists(self.SETUP_DONE_FLAG_FILE):
                os.remove(self.SETUP_DONE_FLAG_FILE)
                
            if os.path.exists(self.USER_SETTINGS_FILE):
                os.remove(self.USER_SETTINGS_FILE)
            
            if os.path.exists(self.KEY_CONFIG_FILE):
                os.remove(self.KEY_CONFIG_FILE)
            
            if os.path.exists(self.CONFIG_DIR):
                os.rmdir(self.CONFIG_DIR)
            
            if os.path.exists(self.LOGS_DIR):
                os.rmdir(self.LOGS_DIR) 
        except IOError as ioe:
            print(repr(ioe))
        except Exception as e:
            print(repr(e))  
                
    def setupFailedEvent(self) -> None:
        self.rollBackSetup()
        self.quit()
        exit(0)
        
    def badField(self, field: str = "both"):
        if field == "both":
            self.api_key_entry.configure(border_color="#ff0555")
            self.username_entry.configure(border_color="#ff0555")
        if field == "username":
            self.username_entry.configure(border_color="#ff0555")   
        if field == "api_key":
            self.api_key_entry.configure(border_color="#ff0555")
        
    def runGUI(self):
        self._gui = gui.WinGTPGUI()
        self.destroy()
        self._gui.mainloop()
        
    def formDoneEvent(self) -> None:
        _valid = False
        
        # Get the username...
        _username = self.username_entry.get()
        # Get the api key...
        _api_key = self.api_key_entry.get()
        
        if len(_username) == 0 and len(_api_key) == 0:
            self.badField("both")
            return False
        
        if len(_username) == 0:
            self.badField("username")
            return False
        else:
            self.USERNAME = _username
            self.config.openConfig()
            self.config.setOption("user", "username", f"{self.USERNAME}")
            self.config.saveConfig()
        
        # Validate the api key...
        if self.validateAPIKey(_api_key):
            self.API_KEY = _api_key
            self.config.openConfig()
            self.config.setOption("user", "api_key", str(_api_key))
            self.config.saveConfig()
            if not self.writeAPIKey(_api_key):
                return False
            else:
                if not self.createSetupDoneFlagFile():
                    self.setupFailedEvent()
                    return False
                else: 
                    _valid = True
        else:
            self.badField("api_key")
            return False

        if _valid == True:
            self.runGUI()
            
    def setup(self) -> bool:
        if not self.createConfigFiles():
            return False
        else:
            self.setupConfig()
            return True
    
    # def setup(self) -> bool: 
    #     if self.createConfigDir(): # 1) Create the root config directory...
    #         if self.createLogsDir(): # 1) Create the logs directory...
    #             if self.createKeyConfigFile(): # 2) Create the file that will hold the api key... 
    #                 dialog = CTkInputDialog(text=f"{self.API_KEY_DIALOG_MESSAGE}", title=f"{self.API_KEY_DIALOG_TITLE}")
    #                 _API_KEY = str(dialog.get_input()) # 3) Get the api key from the user...
    #                 if len(_API_KEY) != 0 and _API_KEY != "None": # 4) Validate the api key...
    #                     try:
    #                         with open(f"{self.KEY_CONFIG_FILE}", "w") as api_key_file:
    #                             if api_key_file.writable():
    #                                 api_key_file.write(_API_KEY) # 5) Hard set the api key...
    #                                 api_key_file.close()
    #                                 self.API_KEY = _API_KEY
    #                                 dialog2 = CTkInputDialog(text=f"{self.USERNAME_DIALOG_MESSAGE}", title=f"{self.USERNAME_DIALOG_TITLE}")
    #                                 _USERNAME = str(dialog2.get_input()) # 7) Get the username from the user...
    #                                 if len(_USERNAME) != 0 and _USERNAME != "None": # 8) Validate the username...
    #                                     self.USERNAME = _USERNAME 
    #                                     if self.createSettingsConfigFile(): # 10) Create the main settings file.
    #                                         if self.createSetupFinishedFlag(): # 11) Create a flag to indicate that setup finished successfuly.
    #                                             if self.setupConfig(): # 12 ) Set default settings in settings.ini
    #                                                 return True
    #                                             else:
    #                                                 self.rollBackSetup() # 1) Roll back steps 12 - 1 if setup failed.
    #                                                 return False
    #                                         else:
    #                                             self.rollBackSetup() # 1) Roll back steps 11 - 1 if setup failed.
    #                                             return False
    #                                     else:
    #                                         self.rollBackSetup() # 1) Roll back steps 10 - 1 if setup failed.
    #                                         return False
    #                                 else:
    #                                     self.rollBackSetup() # 1) Roll back steps 8 - 1 if setup failed.
    #                                     return False
    #                             else:
    #                                 self.rollBackSetup() # 1) Roll back steps 6 - 1 if setup failed.
    #                                 return False
    #                     except FileNotFoundError:
    #                         self.rollBackSetup() # 1) Roll back steps 5 - 1 if setup failed.
    #                         return False
    #                     except IOError:
    #                         self.rollBackSetup() # 1) Roll back steps 5 - 1 if setup failed.
    #                         return False
    #                     except Exception as e:
    #                         print(repr(e))
    #                         self.rollBackSetup() # 1) Roll back steps 5 - 1 if setup failed.
    #                         return False
    #                 else:
    #                     self.rollBackSetup() # 1) Roll back steps 4 - 1 if setup failed.
    #                     return False
    #             else:
    #                 self.rollBackSetup() # 1) Roll back steps 2 - 1 if setup failed.
    #                 return False
    #         else:
    #             self.rollBackSetup() # 1) Roll back steps 1 - 1 if setup failed.
    #             return False
    #     else:
    #         self.rollBackSetup() # 1) Roll back steps 1 - 1 if setup failed.
    #         return False
