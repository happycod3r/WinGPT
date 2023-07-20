import customtkinter
import cli
import persistence
from PIL import Image
import os

customtkinter.set_appearance_mode("dark")


class SetupForm(customtkinter.CTk):
    width = 900
    height = 600

    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.config = persistence.Persistence()
        self.cli = cli.WinGTPCLI()
        
        self.CONFIG_DIR = self.config.CONFIG_DIR
        self.LOGS_DIR = "./logs"
        self.USER_SETTINGS_FILE = self.config.USER_SETTINGS_FILE
        self.KEY_CONFIG_FILE = self.config.KEY_CONFIG_FILE
        self.SETUP_DONE_FLAG_FILE = f"{self.CONFIG_DIR}/.setup.flag"
        self.USERNAME = None
        self.API_KEY = None
        
        self.title("Wingtp & OpenAI Setup")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        # load and create background image
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.bg_image = customtkinter.CTkImage(Image.open(current_path + "/images/bg_gradient.jpg"), size=(self.width, self.height))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        self.setup_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.setup_frame.grid(row=0, column=0, sticky="ns")
        
        self.setup_label = customtkinter.CTkLabel(self.setup_frame, text="WinGTP Setup", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.setup_label.grid(row=0, column=0, padx=30, pady=(150, 15))
        
        self.username_entry = customtkinter.CTkEntry(self.setup_frame, width=200, placeholder_text="username")
        self.username_entry.grid(row=1, column=0, padx=30, pady=(15, 15))
        
        self.api_key_entry = customtkinter.CTkEntry(self.setup_frame, width=200, show="*", placeholder_text="api key")
        self.api_key_entry.grid(row=2, column=0, padx=30, pady=(0, 15))
        
        self.setup_done_button = customtkinter.CTkButton(self.setup_frame, text="Finish Setup", command=self.setup_done_event, width=200)
        self.setup_done_button.grid(row=3, column=0, padx=30, pady=(15, 15))

    def setup_done_event(self):
        self.USERNAME = self.username_entry.get()
        self.API_KEY = self.api_key_entry.get()
        self.destroy()

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
            if self.cli.createFile(f"{self.SETUP_DONE_FLAG_FILE}"):
                return True
            else:
                print("Setup failed and cannot finish!")
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
