import paths
import customtkinter
import modules.persistence as persistence
import modules.stdops as stdops
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
        
        self.stdops = stdops.StdOps()
        self.config = persistence.Persistence()
        
        self.CURRENT_PATH = paths.CURRENT_PATH
        self.CONFIG_DIR = paths.CONFIG_DIR
        self.LOGS_DIR = paths.LOGS_DIR
        self.TMP_DIR = paths.TMP_DIR
        self.SYSTEM_LOG_FILE = paths.SYSTEM_LOG_FILE
        self.CHAT_LOG_FILE = paths.CHAT_LOG_FILE
        self.USER_SETTINGS_FILE = paths.USER_SETTINGS_FILE
        self.KEY_CONFIG_FILE = paths.KEY_CONFIG_FILE
        self.SETUP_DONE_FLAG_FILE = paths.SETUP_DONE_FLAG_FILE
        
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
        
        self.bg_image = customtkinter.CTkImage(Image.open(f"{paths.SETUP_BG_IMAGE}"), size=(self.width, self.height))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        self.setup_frame = ctkframe.CustomTkFrame(self, bg_color="transparent", fg_color="transparent")
        self.setup_frame.grid(row=0, column=0, sticky="ns")
        
        self.setup_label = customtkinter.CTkLabel(self.setup_frame, text="WinGTP 0.1.0", font=customtkinter.CTkFont(size=28, weight="bold"))
        self.setup_label.grid(row=0, column=0, padx=30, pady=(150, 15))
        
        self.username_entry = customtkinter.CTkEntry(self.setup_frame, width=200, placeholder_text="username")
        self.username_entry.grid(row=1, column=0, padx=30, pady=(15, 15))
        
        self.api_key_entry = customtkinter.CTkEntry(self.setup_frame, width=200, placeholder_text="api key")
        self.api_key_entry.grid(row=2, column=0, padx=30, pady=(0, 15))
        
        self.setup_done_button = customtkinter.CTkButton(self.setup_frame, text="Finish Setup", command=self.formDoneEvent, width=200)
        self.setup_done_button.grid(row=3, column=0, padx=30, pady=(15, 15))

    def createSetupDoneFlagFile(self) -> bool:
        if not self.stdops.createFile(self.SETUP_DONE_FLAG_FILE):
            return False
        else:
            return True

    def setupConfig(self) -> None:
        self.config.openConfig()
        self.config.setDefaultSection("DEFAULTS")
        self.config.addSection("system")
        self.config.addOption("system", "new_user", True)
        self.config.addOption("system", "config_dir", f"{self.CONFIG_DIR}")
        self.config.addOption("system", "logs_dir", f"{self.LOGS_DIR}")
        self.config.addOption("system", "tmp_dir", f"{self.TMP_DIR}")
        self.config.addOption("system", "config_file", f"{self.USER_SETTINGS_FILE}")
        self.config.addOption("system", "sys_log", f"{self.SYSTEM_LOG_FILE}")
        self.config.addSection("user")
        self.config.addOption("user", "username", f"{self.USERNAME}")
        self.config.addOption("user", "api_key", f"{self.API_KEY}")
        self.config.addOption("user", "api_key_path", f"{self.KEY_CONFIG_FILE}")
        self.config.addOption("user", "organization", "org-8rsyvRZvyUBHhs4fJqATWK23")
        self.config.addSection("ui")
        self.config.addOption("ui", "color", "#5ae7d6")
        self.config.addOption("ui", "ui_scaling", "100%%")
        self.config.addOption("ui", "theme", "System") 
        self.config.addSection("chat")
        self.config.addOption("chat", "chat_to_file", False)
        self.config.addOption("chat", "chat_log_path", f"{self.CHAT_LOG_FILE}")
        self.config.addOption("chat", "echo_chat", False)
        self.config.addOption("chat", "stream_chat", False)
        self.config.addOption("chat", "use_stop_list", False)
        self.config.addOption("chat", "chat_temperature", 1)
        self.config.addOption("chat", "presence_penalty", 0)
        self.config.addOption("chat", "frequency_penalty", 0)
        self.config.addOption("chat", "best_of", 1)
        self.config.addOption("chat", "timeout", 0)
        self.config.addOption("chat", "chat_engine", "text-davinci-003")
        self.config.addOption("chat", "response_token_limit", 16)
        self.config.addOption("chat", "response_count", 1)
        self.config.addOption("chat", "api_base", "https://api.openai.com/v1")
        self.config.addOption("chat", "api_type", "open_ai")
        self.config.addOption("chat", "api_version", None)
        self.config.addOption("chat", "request_type", 0)
        self.config.addOption("chat", "user_defined_data_file", None)
        self.config.addOption("chat", "jsonl_data_file", None)
        self.config.addSection("stop_lists")
        self.config.addOption("stop_lists", "stop_list1", "a custom stop list")
        self.config.addOption("stop_lists", "stop_list2", "another custom stop list")
        self.config.addSection("requests")
        self.config.addOption("requests", "current_request", None)
        self.config.addOption("requests", "previous_request", None)
        self.config.addSection("responses")
        self.config.addOption("responses", "current_response", None)
        self.config.addOption("responses", "previous_response", None)
        self.config.addSection("translations")
        self.config.addOption("translations", "lang1", None)
        self.config.addOption("translations", "lang2", None)
        self.config.addSection("qa")
        self.config.addOption("qa", "context_1", None )
        self.config.addSection("image_requests")
        self.config.addOption("image_requests", "use_edit", 0)
        self.config.addOption("image_requests", "use_variation", 0)
        self.config.addOption("image_requests", "use_new", 1)
        self.config.addOption("image_requests", "img_path", None)
        self.config.addOption("image_requests", "mask_path", None)
        self.config.addOption("image_requests", "img_size", "256x256")
        self.config.addOption("image_requests", "response_format", "url")
        self.config.addSection("audio_transcription")
        self.config.addOption("audio_transcription", "audio_file", None)
        self.config.addSection("edits")
        self.config.addOption("edits", "instruction", None)
        
        if self.config.saveConfig():
            return True
        else: 
            return False

    def createConfigFiles(self) -> bool:
        if not self.stdops.createDir(self.CONFIG_DIR):
            return False
        elif not self.stdops.createDir(self.LOGS_DIR):
            return False
        elif not self.stdops.createDir(self.TMP_DIR):
            return False
        elif not self.stdops.createFile(self.USER_SETTINGS_FILE):
            return False
        elif not self.stdops.createFile(self.KEY_CONFIG_FILE):
            return False
        elif not self.stdops.createFile(self.SYSTEM_LOG_FILE):
            return False
        elif not self.stdops.createFile(self.CHAT_LOG_FILE):
            return False
        else:
            return True

    def validateAPIKey(self, api_key: str) -> bool:
        if not (api_key.startswith('sk-') and len(api_key) == 51):
            return False
        else:
            return True

    def writeAPIKey(self, api_key: str) -> bool:
        if self.stdops.writeTofile(self.KEY_CONFIG_FILE, api_key):
            return True
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
                
            if os.path.exists(self.CHAT_LOG_FILE):
                os.remove(self.CHAT_LOG_FILE)
            
            if os.path.exists(self.SYSTEM_LOG_FILE):
                os.remove(self.SYSTEM_LOG_FILE)
            
            if os.path.exists(self.CONFIG_DIR):
                os.rmdir(self.CONFIG_DIR)
            
            if os.path.exists(self.LOGS_DIR):
                os.rmdir(self.LOGS_DIR)
                
            if os.path.exists(self.TMP_DIR):
                os.rmdir(self.TMP_DIR)
                 
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
