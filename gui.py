import tkinter as tk
import customtkinter as ctk
from tkinter import simpledialog
from tkinter import colorchooser
from tkinter import filedialog
import tkinter.messagebox
from tkinter import *
import normaltime
import persistence
from chatmemory import memory
from cli import WinGTPCLI
from ctrls import ctktextbox
from PIL import Image
import sys
import os 

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class WinGTPGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self._config = persistence.Persistence()
        self._config.openConfig()
        
        self.CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
        self.CONFIG_DIR = f"{self.CURRENT_PATH}\\config"
        self.GUI_SHOWN_FLAG_FILE = f"{self.CONFIG_DIR}\\.gui.flag"
        self.NEW_USER = self._config.getOption("system", "new_user")
        self.USER = self._config.getOption("user", "username")
        self.API_KEY = self._config.getOption("user", "api_key")
        self.API_KEY_PATH = self._config.getOption("user", "api_key_path")

        #//////////// SETTINGS ////////////
        self._OUTPUT_COLOR = f"{self._config.getOption('ui', 'color')}"
        self.UI_SCALING = self._config.getOption('ui', "ui_scaling")
        self.THEME = self._config.getOption('ui', "theme")
        self.SAVE_CHAT = self._config.getOption("chat", "chat_to_file")
        self.CHAT_LOG_PATH = self._config.getOption("chat", "chat_log_path")
        self.ECHO_CHAT = self.CHAT_LOG_PATH = self._config.getOption("chat", "echo_chat")
        self.STREAM_CHAT = self.CHAT_LOG_PATH = self._config.getOption("chat", "stream_chat")
        self.USE_STOP_LIST = self.CHAT_LOG_PATH = self._config.getOption("chat", "use_stop_list")
        self.CHAT_TEMP = self.CHAT_LOG_PATH = self._config.getOption("chat", "chat_temperature")
        self.CHAT_ENGINE = self.CHAT_LOG_PATH = self._config.getOption("chat", "chat_engine")
        self.RESPONSE_TOKEN_LIMIT = self.CHAT_LOG_PATH = self._config.getOption("chat", "response_token_limit")
        self.RESPONSE_COUNT = self.CHAT_LOG_PATH = self._config.getOption("chat", "response_count")
        self.API_BASE = self.CHAT_LOG_PATH = self._config.getOption("chat", "api_base")
        self.API_VERSION = self.CHAT_LOG_PATH = self._config.getOption("chat", "api_version")
        self.API_TYPE = self.CHAT_LOG_PATH = self._config.getOption("chat", "api_type")
        self.ORGANIZATION = self.CHAT_LOG_PATH = self._config.getOption("chat", "organization")
        self.REQUEST_TYPE = self._config.getOption("chat", "request_type")
        
        self.cli = WinGTPCLI()
        self.nt = normaltime.NormalTime()
        self.width = 1300  # 1100
        self.height = 580
                        
        #//////////// WINDOW ////////////
        self.title("WinGTP Powered by Python & OpenAI")
        self.geometry(f"{self.width}x{self.height}")
        #//////////// GRID LAYOUT (4x4) ////////////
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        #//////////// SIDEBAR ////////////
        self.sidebar = ctk.CTkFrame(self, width=140, corner_radius=0)                            
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)
        self.sidebar.configure(corner_radius=4)
        
        #//////////// SIDEBAR LOGO ////////////
        self.sidebar_logo = ctk.CTkLabel(self.sidebar, text="WinGTP v0.1.0", font=ctk.CTkFont(size=20, weight="bold"))
        self.sidebar_logo.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        #//////////// LOGOUT BUTTON ////////////
        
        self.sidebar_logout_btn = ctk.CTkButton(self.sidebar, state=ctk.DISABLED, command=self.sidebar_logout_btn_event)
        self.sidebar_logout_btn.grid(row=1, column=0, padx=20, pady=10)
        
        #//////////// EXIT BUTTON ////////////
        self.sidebar_exit_btn = ctk.CTkButton(self.sidebar, command=self.sidebar_exit_btn_event)
        self.sidebar_exit_btn.grid(row=2, column=0, padx=20, pady=10)
        
        #//////////// SET API KEY BUTTON ////////////
        self.sidebar_set_key_btn = ctk.CTkButton(self.sidebar, command=self.sidebar_set_key_btn_event)
        self.sidebar_set_key_btn.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar.configure()
        
        #//////////// CHANGE OUTPUT COLOR BUTTON ////////////
        self.change_color_btn_label = ctk.CTkLabel(self.sidebar, text="Output Color", anchor="s")
        self.change_color_btn_label.grid(row=4, column=0, padx=20, pady=(10, 0))
        self.sidebar_change_color_btn = ctk.CTkButton(self.sidebar, command=self.change_output_color_event)
        self.sidebar_change_color_btn.grid(row=5, column=0, padx=20, pady=10)
        
        #//////////// THEME SELECT ////////////
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar, text="Appearance Mode:", anchor="sw")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 10), sticky="s")
        self.appearance_mode_option_menu = ctk.CTkOptionMenu(self.sidebar, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_option_menu.grid(row=7, column=0, padx=20, pady=(0, 10))
        
        #//////////// UI SIZE SCALING SELECT ////////////
        self.scaling_label = ctk.CTkLabel(self.sidebar, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.scaling_option_menu = ctk.CTkOptionMenu(self.sidebar, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_option_menu.grid(row=9, column=0, padx=20, pady=(10, 20))

        #//////////// COMMAND ENTRY ////////////
        self.command_entry = ctk.CTkEntry(self, placeholder_text="Enter a command. Try 'help' for a list of commands.")
        self.command_entry.grid(row=3, column=1, columnspan=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        #//////////// CLEAR BUTTON ////////////
        self.send_btn = ctk.CTkButton(self, fg_color="transparent", border_width=2, command=(self.process_input), text="Send Query")
        self.send_btn.grid(row=3, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        #//////////// SEND BUTTON ////////////
        self.clear_btn = ctk.CTkButton(master=self, fg_color="transparent", border_width=2, command=(self.clearAll), text="Clear")
        self.clear_btn.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        #//////////// OUTPUT BOX ////////////
        self.output_box = ctk.CTkTextbox(self, width=250, font=ctk.CTkFont(size=14, weight='bold'))
        self.output_box.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        #//////////// GTP OPTIONS TAB VIEW ////////////
        self.gtp_options_tabview = ctk.CTkTabview(self, width=250)
        self.gtp_options_tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.gtp_options_tabview.add("Response")
        self.gtp_options_tabview.add("API")
        self.gtp_options_tabview.add("Data")
        self.gtp_options_tabview.tab("Response").grid_columnconfigure(0, weight=1)
        self.gtp_options_tabview.tab("API").grid_columnconfigure(0, weight=1)
        self.gtp_options_tabview.tab("Data").grid_columnconfigure(0, weight=1)
        
        self.cli.setAPIKeyPath(self.API_KEY_PATH)
        self.engine_option_menu = ctk.CTkOptionMenu(
            self.gtp_options_tabview.tab("Response"), 
            dynamic_resizing=False, 
            values=self.cli.getEngines(), #["Value 1", "Value 2", "Value 3"]
            command=self.on_engine_option_chosen_event
        )
        self.engine_option_menu.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        #//////////// RESPONSE TOKEN LIMIT INPUT ////////////
        self.response_token_limit_input = ctk.CTkButton(self.gtp_options_tabview.tab("Response"), text=f"Response Token Limit ({self.RESPONSE_TOKEN_LIMIT})", command=self.open_response_token_limit_input_dialog_event)
        self.response_token_limit_input.grid(row=1, column=0, padx=20, pady=(10, 10))
        
        #//////////// RESPONSE COUNT INPUT ////////////
        self.response_count_input = ctk.CTkButton(self.gtp_options_tabview.tab("Response"), text=f"Response Count ({self.RESPONSE_COUNT})", command=self.open_response_count_input_dialog_event)
        self.response_count_input.grid(row=2, column=0, padx=20, pady=(10, 10))

        #//////////// API BASE INPUT ////////////
        self.api_base_input = ctk.CTkButton(self.gtp_options_tabview.tab("API"), text="API Base", command=self.open_api_base_input_dialog_event)
        self.api_base_input.grid(row=0, column=0, padx=20, pady=(10, 10))
        
        #//////////// API TYPE INPUT ////////////
        self.api_type_input = ctk.CTkButton(self.gtp_options_tabview.tab("API"), text="API Type", command=self.open_api_type_input_dialog_event)
        self.api_type_input.grid(row=1, column=0, padx=20, pady=(10, 10))
        
        #//////////// API VERSION INPUT ////////////
        self.api_version_input = ctk.CTkButton(self.gtp_options_tabview.tab("API"), text="API Version", command=self.open_api_version_input_dialog_event)
        self.api_version_input.grid(row=2, column=0, padx=20, pady=(10, 10))
        
        #//////////// ORGANIZATION INPUT ////////////
        self.organization_input = ctk.CTkButton(self.gtp_options_tabview.tab("Data"), text="Organization", command=self.open_organization_input_dialog_event)
        self.organization_input.grid(row=0, column=0, padx=20, pady=(10, 10))
        
        #//////////// USER DEFINED DATA FILE INPUT ////////////
        self.user_defined_datafile_input = ctk.CTkButton(self.gtp_options_tabview.tab("Data"), text="User Defined Data-File", command=self.open_user_defined_datafile_input_dialog_event)
        self.user_defined_datafile_input.grid(row=1, column=0, padx=20, pady=(10, 10))
        
        #//////////// JSONL DATA FILE INPUT ////////////
        self.jsonl_data_file_input = ctk.CTkButton(self.gtp_options_tabview.tab("Data"), text="JSONL Data File", command=self.open_jsonl_datafile_input_dialog_event)
        self.jsonl_data_file_input.grid(row=2, column=0, padx=20, pady=(10, 10))
    
        #//////////// OUTPUT TEMPERATURE RADIO GROUP ////////////
    
        self.output_temp_radiobutton_frame = ctk.CTkFrame(self)
        self.output_temp_radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.output_temp_radio_var = tkinter.IntVar(value=0)
    
        self.output_temp_label_radio_group = ctk.CTkLabel(
            master=self.output_temp_radiobutton_frame, 
            text="Chat Output Temperature"
        )
        self.output_temp_label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        
        self.temp_high_radio_button = ctk.CTkRadioButton(
            master=self.output_temp_radiobutton_frame, 
            text="high", 
            variable=self.output_temp_radio_var, 
            value=self.cli.temps["high"], 
            command=self.output_temp_radio_btn_selected
        )
        self.temp_high_radio_button.grid(row=1, column=2, pady=10, padx=20, sticky="nw")
        
        self.temp_high_color_box = ctk.CTkEntry(master=self.output_temp_radiobutton_frame, width=40, border_width=0)
        self.temp_high_color_box.grid(row=1, column=3, sticky="e")
        
        self.temp_medium_radio_button = ctk.CTkRadioButton(
            master=self.output_temp_radiobutton_frame, 
            text="medium", 
            variable=self.output_temp_radio_var, 
            value=self.cli.temps["medium"], 
            command=self.output_temp_radio_btn_selected
        )
        self.temp_medium_radio_button.grid(row=2, column=2, pady=10, padx=20, sticky="nw")
        
        self.temp_medium_color_box = ctk.CTkEntry(master=self.output_temp_radiobutton_frame, width=40, border_width=0)
        self.temp_medium_color_box.grid(row=2, column=3, sticky="e")
        
        self.temp_low_radio_button = ctk.CTkRadioButton(
            master=self.output_temp_radiobutton_frame, 
            variable=self.output_temp_radio_var, 
            value=self.cli.temps["low"], 
            command=self.output_temp_radio_btn_selected
        )
        self.temp_low_radio_button.grid(row=3, column=2, pady=10, padx=20, sticky="nw")
        
        self.temp_low_color_box = ctk.CTkEntry(master=self.output_temp_radiobutton_frame, width=40, border_width=0)
        self.temp_low_color_box.grid(row=3, column=3, sticky="e")
        
        #//////////// INPUT BOX FRAME ////////////
        self.input_box_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_box_frame.grid(row=1, column=1, padx=(20, 0), pady=(0, 0), sticky="nsew")
        self.input_box_frame.grid_columnconfigure(0, weight=1)
        self.input_box_frame.grid_rowconfigure(0, weight=1)
        
        #//////////// INPUT BOX ////////////
        self.input_box = ctktextbox.CustomTkTextbox(
            self.input_box_frame, 
            font=ctk.CTkFont('Segoi UI', size=16)
        )
        self.input_box.grid(row=0, column=0, sticky='nsew')

        #//////////// SETTINGS SWITCHES ////////////
        self.settings_switches_frame = ctk.CTkScrollableFrame(self, label_text="Turn Settings on/off")
        self.settings_switches_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.settings_switches_frame.grid_columnconfigure(0, weight=1)
        
        #//////////// CHAT ECHO ////////////    
        self.chat_echo_switch = ctk.CTkSwitch(master=self.settings_switches_frame, text=f"Echo", command=self.on_chat_echo_switch_changed_event)
        self.chat_echo_switch.grid(row=0, column=0, padx=10, pady=(0, 20))
        
        #//////////// CHAT STREAM ////////////
        self.chat_stream_switch = ctk.CTkSwitch(master=self.settings_switches_frame, text=f"Stream", command=self.on_chat_stream_switch_changed_event)
        self.chat_stream_switch.grid(row=1, column=0, padx=10, pady=(0, 20))
        
        #//////////// STOP LIST ////////////
        self.chat_stop_list_switch = ctk.CTkSwitch(master=self.settings_switches_frame, text=f"Stop List", command=self.on_chat_stop_list_switch_changed_event)
        self.chat_stop_list_switch.grid(row=2, column=0, padx=10, pady=(0, 20))
        
        #//////////// WRITE CHAT ////////////
        self.save_chat_switch = ctk.CTkSwitch(master=self.settings_switches_frame, text=f"Save Chat", command=self.on_save_chat_switch_changed_event)
        self.save_chat_switch.grid(row=3, column=0, padx=10, pady=(0, 20))

        #//////////// REQUEST TYPE RADIO GROUP ////////////
        self.request_type_slider_frame = ctk.CTkScrollableFrame(self)
        self.request_type_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.request_type_slider_frame.grid_columnconfigure(0, weight=1)
        self.request_type_radio_var = tkinter.IntVar(value=0)
        
        self.output_request_type_radio_group = ctk.CTkLabel(
            master=self.request_type_slider_frame, 
            text="Request Types"
        )
        self.output_request_type_radio_group.grid(row=0, column=0, columnspan=1, sticky="nsew")
        
        self.chat_radio_btn = ctk.CTkRadioButton(
            master=self.output_request_type_radio_group,
            text="Chat",
            variable=self.request_type_radio_var,
            value=self.cli.request_types["chat"],
            command=self.request_type_radio_btn_selected
        )
        self.chat_radio_btn.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="nw")
        
        self.images_radio_btn = ctk.CTkRadioButton(
            master=self.output_request_type_radio_group,
            text="Images",
            variable=self.request_type_radio_var,
            value=self.cli.request_types["images"],
            command=self.request_type_radio_btn_selected
            
        )
        self.images_radio_btn.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="nw")
        
        self.audio_radio_btn = ctk.CTkRadioButton(
            master=self.output_request_type_radio_group,
            text="Audio",
            variable=self.request_type_radio_var,
            value=self.cli.request_types["audio"],
            command=self.request_type_radio_btn_selected
            
        )
        self.audio_radio_btn.grid(row=3, column=0, pady=(20, 0), padx=20, sticky="nw")
        
        self.embeddings_radio_btn = ctk.CTkRadioButton(
            master=self.output_request_type_radio_group,
            text="Embeddings",
            variable=self.request_type_radio_var,
            value=self.cli.request_types["embeddings"],
            command=self.request_type_radio_btn_selected
        )
        self.embeddings_radio_btn.grid(row=4, column=0, pady=(20, 0), padx=20, sticky="nw")
        
        self.files_radio_btn = ctk.CTkRadioButton(
            master=self.output_request_type_radio_group,
            text="Files",
            variable=self.request_type_radio_var,
            value=self.cli.request_types["files"],
            command=self.request_type_radio_btn_selected
        )
        self.files_radio_btn.grid(row=5, column=0, pady=(20, 0), padx=20, sticky="nw")
        
        self.fine_tuning_radio_btn = ctk.CTkRadioButton(
            master=self.output_request_type_radio_group,
            text="Fine Tuning",
            variable=self.request_type_radio_var,   
            value=self.cli.request_types["fine_tuning"], 
            command=self.request_type_radio_btn_selected
        )
        self.fine_tuning_radio_btn.grid(row=6, column=0, pady=(20, 0), padx=20, sticky="nw")
        
        self.moderations_radio_btn = ctk.CTkRadioButton(
            master=self.output_request_type_radio_group,
            text="Moderations",
            variable=self.request_type_radio_var,
            value=self.cli.request_types["moderations"],
            command=self.request_type_radio_btn_selected
        )
        self.moderations_radio_btn.grid(row=7, column=0, pady=(20, 0), padx=20, sticky="nw")
        
        self.build_request_radio_btn = ctk.CTkRadioButton(
            master=self.output_request_type_radio_group,
            text="Build Requests",
            variable=self.request_type_radio_var,
            value=self.cli.request_types["build_requests"],
            command=self.request_type_radio_btn_selected    
        )
        self.build_request_radio_btn.grid(row=8, column=0, pady=(20, 0), padx=20, sticky="nw")

        #//////////// DEFAULT VALUES ////////////
        self.sidebar_logout_btn.configure(state="normal", text="Logout")
        self.sidebar_exit_btn.configure(state="normal", text="Exit")
        self.sidebar_set_key_btn.configure(state="normal", text="API Key")
        self.sidebar_change_color_btn.configure(state="normal", text="Color")

        self.temp_high_radio_button.configure(text="( 2 ) High")
        self.temp_medium_radio_button.configure(text="( 1 ) Medium")
        self.temp_low_radio_button.configure(text="( 0 ) Low")
        
        #////// GUI LOADED //////
        self.loadOptions()
        self._config.saveConfig()
        self.setGUIShownFlag()
        self.setOutput(self.cli.greetUser(self.USER, self.API_KEY_PATH), "chat")
        #//////////// GUI METHODS ////////////

    def setGUIShownFlag(self):
        self.cli.createFile(self.GUI_SHOWN_FLAG_FILE)
    
    def loadOptions(self):
        self.output_box.configure(text_color=self._OUTPUT_COLOR)
        self.send_btn.configure(border_color=self._OUTPUT_COLOR)
        self.clear_btn.configure(border_color=self._OUTPUT_COLOR)
        self.command_entry.configure(border_color=self._OUTPUT_COLOR)
        self.sidebar_logo.configure(text_color=self._OUTPUT_COLOR)
        self.appearance_mode_label.configure(text_color=self._OUTPUT_COLOR)
        self.scaling_label.configure(text_color=self._OUTPUT_COLOR)
        self.output_temp_label_radio_group.configure(text_color=self._OUTPUT_COLOR)
        self.change_color_btn_label.configure(text_color=self._OUTPUT_COLOR)
        self.settings_switches_frame.configure(label_text_color=self._OUTPUT_COLOR)
        self.output_request_type_radio_group.configure(text_color=self._OUTPUT_COLOR)
        
        if self._config.getOption("chat", "echo_chat") == "True":
            self.chat_echo_switch.select()
            self.ECHO_CHAT = True
            
        if self._config.getOption("chat", "stream_chat") == "True":
            self.chat_stream_switch.select()
            self.CHAT_LOG_PATH = self._config.getOption("chat", "chat_log_path")

        if self._config.getOption("chat", "use_stop_list") == "True":
            self.chat_stop_list_switch.select()
            self.USE_STOP_LIST = True
            
        if self._config.getOption("chat", "chat_to_file") == "True":
            self.save_chat_switch.select()
            self.SAVE_CHAT = True         
            
        if self._config.getOption("chat", "stream_chat") == "True":
            self.chat_stream_switch.select()
            self.STREAM_CHAT = True
            
        #////// OUTPUT TEMP RADIO GROUP
        output_temp = int(self._config.getOption("chat", "chat_temperature"))
        if output_temp == 0:
            self.temp_low_radio_button.select()
            self.output_temp_radio_btn_selected()
        elif output_temp == 1:
            self.temp_medium_radio_button.select()
            self.output_temp_radio_btn_selected()
        else:
            self.temp_high_radio_button.select()
            self.output_temp_radio_btn_selected()
            
        self.engine_option_menu.set(self._config.getOption("chat", "chat_engine"))
        self.appearance_mode_option_menu.set(self._config.getOption("ui", "theme"))
        self.scaling_option_menu.set(self._config.getOption("ui", "ui_scaling"))
        
    def clearAll(self):
        self.clearInput()
        self.clearOutput()
        self.command_entry.delete(0, tk.END)     
    
    def on_save_chat_switch_changed_event(self) -> None:
        state = self.save_chat_switch.get()
        if state == 0:
            self.SAVE_CHAT = False
            self.setOutput("[Save chat]: Off", "cli")
            self._config.openConfig()
            self._config.setOption("chat", "chat_to_file", False)
            self._config.saveConfig()
        else:
            if self.CHAT_LOG_PATH == None:
                self.CHAT_LOG_PATH = self.openFileDialog()
                self.SAVE_CHAT = True
                self.setOutput("[Save chat]: On", "cli")
            else:
                self.SAVE_CHAT = True
                self.setOutput("[Save chat]: On", "cli")
            self._config.openConfig()
            self._config.setOption("chat", "chat_to_file", True)
            self._config.setOption("chat", "chat_log_path", self.CHAT_LOG_PATH)
            self._config.saveConfig()
            
    def openFileDialog(self) -> (str | bool):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.setOutput(f"Selected file: {file_path}", "cli")
            return file_path
        else:
            self.setOutput(f"No file selected", "cli")
            return False
            
    def on_chat_echo_switch_changed_event(self) -> None:
        state = self.chat_echo_switch.get()
        if state == 0:
            self.cli.setChatEcho(False)
            self.setOutput("[Chat echo]: Off", "cli")
            self._config.openConfig()
            self._config.setOption("chat", "echo_chat", False)
            self._config.saveConfig()
        else:
            self.cli.setChatEcho(True)
            self.setOutput("[Chat echo]: On", "cli")
            self._config.openConfig(    )
            self._config.setOption("chat", "echo_chat", True)
            self._config.saveConfig()

    def on_chat_stream_switch_changed_event(self) -> None:
        state = self.chat_stream_switch.get()
        if state == 0:
            self.cli.setChatStream(False)
            self.setOutput("[Chat stream]: Off", "cli")
            self._config.openConfig()
            self._config.setOption("chat", "stream_chat", False)
            self._config.saveConfig()
        else:
            self.cli.setChatStream(True)
            self.setOutput("[Chat stream]: On", "cli")
            self._config.openConfig()
            self._config.setOption("chat", "stream_chat", True)
            self._config.saveConfig()
            
    def on_chat_stop_list_switch_changed_event(self) -> None:
        state = self.chat_stop_list_switch.get()
        if state == 0:
            self.setOutput("[Chat stop list]: Off", "cli")
            self._config.openConfig()
            self._config.setOption("chat", "use_stop_list", False)
            self._config.saveConfig()
        else:
            dialog = ctk.CTkInputDialog(text="Enter a list of words you want the output to stop at if encountered\nWords should be quoted!: ", title="Chat Stop List")
            _stoplist = str(dialog.get_input())
            if len(_stoplist) != 0 and _stoplist != "None":
                self.cli.setStopList(_stoplist)
                self.setOutput("[Chat stop list]: On", "cli")
                self._config.openConfig()
                self._config.setOption("chat", "use_stop_list", True)
                self._config.saveConfig()
                return True
            else:
                self._config.openConfig()
                self._config.setOption("chat", "use_stop_list", False)
                self._config.saveConfig()
                return False
            
    def on_engine_option_chosen_event(self, engine) -> None:
        self.cli.setEngine(f"{engine}")
        self.CHAT_ENGINE = engine
        self.setOutput(f"Engine changed to: {engine}", "cli")
        self._config.openConfig()
        self._config.setOption("chat", "chat_engine", f"{self.CHAT_ENGINE}")
        self._config.saveConfig()
            
    def open_jsonl_datafile_input_dialog_event(self) -> bool:
        dialog = ctk.CTkInputDialog(text="Enter a .jsonl file path: ", title="JSONL Data File Input")
        path = str(dialog.get_input())
        if path == "None":
            return False
        if len(path) != 0:
            if os.path.exists(path):
                self.cli.setJSONLDataFile(path)
                self.setOutput(f"File set: [{self.cli.getJSONLDataFile()}]", "cli")
                return True
            else:
                self.setOutput(f"File doesn\'t exist! [{path}]", "cli")
                return False
        return False
 
    def open_user_defined_datafile_input_dialog_event(self) -> bool:
        dialog = ctk.CTkInputDialog(text="Enter a file path: ", title="User Defined Data File Input")
        path = str(dialog.get_input())
        if path == "None":
            return False
        if len(path) != 0:
            if os.path.exists(path):
                self.cli.setUserDefinedFileName(path)
                self.setOutput(f"File set: [{self.cli.getUserDefinedFileName()}]", "cli")
                return True
            else:
                self.setOutput(f"File doesn\'t exist! [{path}]", "cli")
                return False
            return False
  
    def open_organization_input_dialog_event(self) -> bool:
        dialog = ctk.CTkInputDialog(text="Enter organization: ", title="Organization Input")
        organization = str(dialog.get_input())
        if len(organization) != 0 and organization != "None":
            self.cli.setOrganization(organization)
            self.ORGANIZATION = organization
            self.setOutput(f"Organization changed to: [{self.cli.getOrganization()}]", "cli")
            self._config.openConfig()
            self._config.setOption("chat", "organization", self.ORGANIZATION)
            self._config.saveConfig()
            return True
        else:
            return False
        
    def open_api_version_input_dialog_event(self) -> bool:
        dialog = ctk.CTkInputDialog(text="Enter the API version: ", title="API Version Input")
        api_version = str(dialog.get_input())
        if len(api_version) != 0 and api_version != "None":
            self.cli.setAPIVersion(api_version)
            self.API_VERSION = api_version
            self.setOutput(f"API version changed to: [{self.cli.getAPIVersion()}]", "cli")
            self._config.openConfig()
            self._config.setOption("chat", "api_version", self.API_VERSION)
            self._config.saveConfig()
            return True
        else:
            return False
            
    def open_api_type_input_dialog_event(self) -> bool:
        dialog = ctk.CTkInputDialog(text="Enter the API type: ", title="API Type Input")
        api_type = str(dialog.get_input())
        if len(api_type) != 0 and api_type != "None":
            self.cli.setAPIType(api_type)
            self.API_TYPE = api_type
            self.setOutput(f"API type changed to: [{self.cli.getAPIType()}]", "cli")
            self._config.openConfig()
            self._config.setOption("chat", "api_type", self.API_TYPE)
            self._config.saveConfig()
            return True
        else:
            return False

    def open_api_base_input_dialog_event(self) -> bool:
        dialog = ctk.CTkInputDialog(text="Enter the API base: ", title="API Base Input")
        api_base = str(dialog.get_input())
        if len(api_base) != 0 and api_base != "None":
            self.cli.setAPIBase(api_base)
            self.API_BASE = api_base
            self.setOutput(f"API base changed to: [{self.cli.getAPIBase()}]", "cli")
            self._config.openConfig()
            self._config.setOption("chat", "api_base", self.API_BASE)
            self._config.saveConfig()
            return True
        else:
            return False

    def open_response_token_limit_input_dialog_event(self) -> bool: 
        dialog = ctk.CTkInputDialog(text="Enter the response token limit: ", title="Response Token Limit Input")
        token_limit = str(dialog.get_input())
        if token_limit.isdigit() and token_limit != "None":
            self.cli.setResponseTokenLimit(token_limit)
            self.RESPONSE_TOKEN_LIMIT = token_limit
            self.setOutput(f"Response token limit changed to: [{self.cli.getResponseTokenLimit()}]", "cli")
            self.response_token_limit_input.configure(text=f"Response Token Limit ({self.RESPONSE_TOKEN_LIMIT})")
            self._config.openConfig()
            self._config.setOption("chat", "response_token_limit", self.RESPONSE_TOKEN_LIMIT)
            self._config.saveConfig()
            return True
        else:
            return False
        
    def open_response_count_input_dialog_event(self) -> bool:
        dialog = ctk.CTkInputDialog(text="Enter the response count: ", title="Response Count Input")
        response_count = str(dialog.get_input())
        if response_count.isdigit() and response_count != "None":
            self.cli.setResponseCount(response_count)
            self.RESPONSE_COUNT = response_count
            self.setOutput(f"Response count changed to: [{self.cli.getResponseCount()}]", "cli")
            self.response_count_input.configure(text=f"Response Count ({self.RESPONSE_COUNT})")
            self._config.openConfig()
            self._config.setOption("chat", "response_count", self.RESPONSE_COUNT)
            self._config.saveConfig()
            return True
        else:
            return False
    
    def request_type_radio_btn_selected(self):
        selected_value = self.request_type_radio_var.get()
        if selected_value == self.cli.request_types["chat"]:
            self.cli.setRequestType(selected_value)
            self.REQUEST_TYPE = selected_value
            self.setOutput(f"Request type changed to: ({selected_value})", "cli")
            self._config.openConfig()
            self._config.setOption("chat", "request_type", self.REQUEST_TYPE)
            self._config.saveConfig()
        elif selected_value == self.cli.request_types["images"]:
            self.cli.setRequestType(selected_value)
            self.REQUEST_TYPE = selected_value
            self.setOutput(f"Request type changed to: ({selected_value})", "cli")
            self._config.openConfig()
            self._config.setOption("chat", "request_type", self.REQUEST_TYPE)
            self._config.saveConfig()
        elif selected_value == self.cli.request_types["audio"]:
            self.cli.setRequestType(selected_value)
            self.REQUEST_TYPE = selected_value
            self.setOutput(f"Request type changed to: ({selected_value})", "cli")
            self._config.openConfig()
            self._config.setOption("chat", "request_type", self.REQUEST_TYPE)
            self._config.saveConfig()
        elif selected_value == self.cli.request_types["embeddings"]:
            self.cli.setRequestType(selected_value)
            self.REQUEST_TYPE = selected_value
            self.setOutput(f"Request type changed to: ({selected_value})", "cli")
            self._config.openConfig()
            self._config.setOption("chat", "request_type", self.REQUEST_TYPE)
            self._config.saveConfig()
        elif selected_value == self.cli.request_types["files"]:
            self.cli.setRequestType(selected_value)
            self.REQUEST_TYPE = selected_value
            self.setOutput(f"Request type changed to: ({selected_value})", "cli")
            self._config.openConfig()
            self._config.setOption("chat", "request_type", self.REQUEST_TYPE)
            self._config.saveConfig()
        elif selected_value == self.cli.request_types["fine_tuning"]:
            self.cli.setRequestType(selected_value)
            self.REQUEST_TYPE = selected_value
            self.setOutput(f"Request type changed to: ({selected_value})", "cli")
            self._config.openConfig()
            self._config.setOption("chat", "request_type", self.REQUEST_TYPE)
            self._config.saveConfig()
        elif selected_value == self.cli.request_types["moderations"]:
            self.cli.setRequestType(selected_value)
            self.REQUEST_TYPE = selected_value
            self.setOutput(f"Request type changed to: ({selected_value})", "cli")
            self._config.openConfig()
            self._config.setOption("chat", "request_type", self.REQUEST_TYPE)
            self._config.saveConfig()
        elif selected_value == self.cli.request_types["build_requests"]:
            self.cli.setRequestType(selected_value)
            self.REQUEST_TYPE = selected_value
            self.setOutput(f"Request type changed to: ({selected_value})", "cli")
            self._config.openConfig()
            self._config.setOption("chat", "request_type", self.REQUEST_TYPE)
            self._config.saveConfig()
    
    def output_temp_radio_btn_selected(self) -> bool:
        selected_value = self.output_temp_radio_var.get()
        if selected_value == self.cli.temps["high"]:
            self.cli.setTemperature(selected_value)
            self.CHAT_TEMP = selected_value
            self.temp_high_color_box.configure(fg_color="#ff2044", text_color="#000000")
            self.temp_medium_color_box.configure(fg_color="#343638")
            self.temp_low_color_box.configure(fg_color="#343638")
            self.setOutput(f"Temperature changed to: High ({selected_value})", "cli")
            self._config.openConfig()
            self._config.setOption("chat", "chat_temperature", self.CHAT_TEMP)
            self._config.saveConfig()
        elif selected_value == self.cli.temps["medium"]:
            self.cli.setTemperature(selected_value)
            self.CHAT_TEMP = selected_value
            self.temp_high_color_box.configure(fg_color="#343638")
            self.temp_medium_color_box.configure(fg_color="#ffe033", text_color="#000000")
            self.temp_low_color_box.configure(fg_color="#343638")
            self.setOutput(f"Temperature changed to: Medium ({selected_value})", "cli")
            self._config.openConfig()
            self._config.setOption("chat", "chat_temperature", self.CHAT_TEMP)
            self._config.saveConfig()
        elif selected_value == self.cli.temps["low"]:
            self.cli.setTemperature(selected_value)
            self.CHAT_TEMP = selected_value
            self.temp_high_color_box.configure(fg_color="#343638")
            self.temp_medium_color_box.configure(fg_color="#343638")
            self.temp_low_color_box.configure(fg_color="#10ba5d", text_color="#000000")
            self.setOutput(f"Temperature changed to: Low ({selected_value})", "cli")
            self._config.openConfig()
            self._config.setOption("chat", "chat_temperature", self.CHAT_TEMP)
            self._config.saveConfig()   
        
    def change_appearance_mode_event(self, _new_appearance_mode: str) -> bool:
        _theme = _new_appearance_mode
        if len(_theme) != 0 and _theme != "None":
            ctk.set_appearance_mode(_theme)
            self.THEME = _theme
            self.setOutput(f"Appearance mode changed to: {self.THEME}", "cli")
            self._config.openConfig()
            self._config.setOption("ui", "theme", self.THEME)
            self._config.saveConfig()
            return True
        else:
            self.setOutput(f"Appearance mode: {_theme} doesn\'t exist!\nOptions are [Light|Dark|System]", "cli")
            return False
            
    def change_output_color_event(self) -> None:
        color = colorchooser.askcolor(title="Select Color")
        self._OUTPUT_COLOR = f"{color[1]}"
        self.output_box.configure(text_color=self._OUTPUT_COLOR)
        self.send_btn.configure(border_color=self._OUTPUT_COLOR)
        self.clear_btn.configure(border_color=self._OUTPUT_COLOR)
        self.command_entry.configure(border_color=self._OUTPUT_COLOR)
        self.sidebar_logo.configure(text_color=self._OUTPUT_COLOR)
        self.appearance_mode_label.configure(text_color=self._OUTPUT_COLOR)
        self.scaling_label.configure(text_color=self._OUTPUT_COLOR)
        self.output_temp_label_radio_group.configure(text_color=self._OUTPUT_COLOR)
        self.change_color_btn_label.configure(text_color=self._OUTPUT_COLOR)
        self.settings_switches_frame.configure(label_text_color=self._OUTPUT_COLOR)
        self.output_request_type_radio_group.configure(text_color=self._OUTPUT_COLOR)
     
        self._config.openConfig()
        self._config.setOption("ui", "color", f"{self._OUTPUT_COLOR}")
        self._config.saveConfig()
               
    def change_scaling_event(self, new_scaling: str) -> None:
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        self.UI_SCALING = new_scaling_float
        ctk.set_widget_scaling(new_scaling_float)
        self._config.openConfig()
        self._config.setOption("ui", "chat_temperature", f"{self.UI_SCALING}%%")
        self._config.saveConfig()

    def sidebar_logout_btn_event(event) -> None:
        pass
    
    def sidebar_exit_btn_event(self) -> None:
        sys.exit(0)
 
    def sidebar_set_key_btn_event(self) -> None:
        dialog = ctk.CTkInputDialog(text=f"{self.USER} enter your OpenAI API key: ", title="API Key")
        api_key = str(dialog.get_input())
        self.cli.setAPIKey(api_key)
        if self.cli.setAPIKey(api_key):
            if self.cli.validateAPIKey(api_key):
                self.API_KEY = api_key
                self.setOutput("Api key has been set successfully!", "cli")
                self._config.openConfig()
                self._config.setOption("user", "api_key", f"{self.API_KEY}")
                self._config.saveConfig()
            else:
                self.setOutput("API key is not valid!", "cli")
        else:
            self.setOutput("Api key was not set!", "cli")
                 
    def clearInput(self) -> None:
        self.input_box.delete("1.0", tk.END)
    
    def clearOutput(self) -> None:
        self.output_box.delete("1.0", tk.END)
        self.clearInput()
    
    def getUserInput(self) -> str:
        user_query_input = self.input_box.get("1.0", tk.END).strip()
        user_cmd_input = self.command_entry.get()
        inputs = {
            "query": user_query_input, 
            "command": user_cmd_input      
        }
        return inputs

    def setOutput(self, output: str, type: str = "cli") -> None:
        if type == "chat":
            self.output_box.insert(tk.END, f"\n{self.nt.time(False)} [{self.cli.engine}]: {output}\n")
        elif type == "cli":
            self.output_box.insert(tk.END, f"\n{self.nt.time(False)} [wingtp]: {output}\n")
        elif type == "user":
            self.output_box.insert(tk.END, f"\n{self.nt.time(False)} [{self.USER}]: {output}\n")

    def getUsername(self) -> str:
        self._config.openConfig()
        self.USER = self._config.getOption("user", "username")
        self._config.saveConfig()

    def setUsername(self) -> None:
        username = simpledialog.askstring('Enter a username that you would like to use: ')
        self.USER = username
        self._config.openConfig()
        self._config.setOption("user", "username", username)

    def processQueryRequest(self, request: str) -> bool:
        self.cli.setAPIKeyPath(self.API_KEY_PATH)
        self.cli.setEngine(self.cli.engine)
        self.cli.setResponseTokenLimit(self.cli.response_token_limit)
        self.cli.setResponseCount(self.cli.response_count)
        self.cli.setRequest(request)
        self.cli.requestData()
        response = self.cli.getResponse()
        self.clearInput()
        self.setOutput(request, "user")
        self.setOutput(response, "chat")
        if self.SAVE_CHAT:
            if self.cli.saveChat(self.CHAT_LOG_PATH, f"{request}\n{response}\n") != False:
                return True
            else:
                return False
    
    def processCommandRequest(self, request: str) -> None:
        if self.SAVE_CHAT:
            self.cli.saveChat(self.CHAT_LOG_PATH, f"{request}")
        if request == self.cli.cli_options[0]:
            self.setOutput("Goodbye! ...", "cli")
            sys.exit()
        elif request == self.cli.cli_options[1]:
            self.open_response_token_limit_input_dialog_event()
            self.clearInput()
        elif request == self.cli.cli_options[2]:
            engine = simpledialog.askstring("Input", "Set the engine: ")
            self.cli.setEngine(engine)
            self.clearInput()
            self.setOutput(f"Engine set to {self.cli.getEngine()}", "cli")
        elif request == self.cli.cli_options[3]:
            self.open_response_count_input_dialog_event()
            self.clearInput()
        elif request == self.cli.cli_options[4]:
            self.open_api_base_input_dialog_event()
            self.clearInput()
        elif request == self.cli.cli_options[5]:
            self.open_api_type_input_dialog_event()
            self.clearInput()
        elif request == self.cli.cli_options[6]:
            self.open_api_version_input_dialog_event()
            self.clearInput()
        elif request == self.cli.cli_options[7]:
            self.open_organization_input_dialog_event()
            self.clearInput()
        elif request == self.cli.cli_options[8]:
            self.open_user_defined_datafile_input_dialog_event()
            self.clearInput()
        elif request == self.cli.cli_options[9]:
            self.open_jsonl_datafile_input_dialog_event()
            self.clearInput()
        elif request == self.cli.cli_options[10]:
            self.clearInput()
            self.setOutput(self.cli._help.__doc__, "cli")
        elif request == self.cli.cli_options[11]:
            self.clearOutput()
        elif request.split(' ')[0] == self.cli.cli_options[12]:
            self.change_appearance_mode_event(request.split(' ')[1])
        elif request == self.cli.cli_options[13]:
            self.change_output_color_event()
        else:
            self.setOutput(self.cli._help.__doc__, "cli")
    
    def process_input(self) -> None:
        request = self.getUserInput()
        query_request = request["query"]
        command_request = request["command"]
        if len(query_request) != 0:
            self.processQueryRequest(query_request)
        if len(command_request) != 0:
            self.processCommandRequest(command_request)
        if len(query_request) == 0 and len(command_request) == 0:
            self.setOutput(f" \
Try entering text into the chat window to receive a reponse.\n \
Or you can use one of the following commands by entering one\n \
into the command input under the chat window.\n \
{self.cli._help.__doc__}", "cli")


    