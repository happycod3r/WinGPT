import tkinter as tk
import customtkinter as ctk
from tkinter import simpledialog
from tkinter import colorchooser
import tkinter.messagebox
from tkinter import *
from bin import normaltime
from chatmemory import memory
from wingtp_cli import WinGTPCLI
from ctrls import ctktextbox
from PIL import Image
import sys
import os 

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class WinGTPGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        #//////////// WINGTP GUI PROPERTIES ////////////
        self.USER = sys.argv[1]
        self.API_KEY_PATH = './config/.api_key.conf'
        self.wingtp_cli = WinGTPCLI()
        self.nt = normaltime.NormalTime()
        self.width = 1300  # 1100
        self.height = 580
        self._OUTPUT_COLOR = "#DCE4EE"
        
        #//////////// WINDOW ////////////
        self.title("WinGTP Powered by Python & OpenAI")
        self.geometry(f"{self.width}x{self.height}")
        #//////////// GRID LAYOUT (4x4) ////////////
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        #//////////// BACKGROUND IMAGE ////////////
        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.bg_image = ctk.CTkImage(Image.open(
            self.current_path + "./images/bg_gradient.jpg"), 
            size=(self.width, self.height)
        )
        
    
        #//////////// SIDEBAR ////////////
        self.sidebar = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)
        
        #//////////// SIDEBAR LOGO ////////////
        self.sidebar_logo = ctk.CTkLabel(self.sidebar, text="WinGTP v0.1.0", font=ctk.CTkFont(size=20, weight="bold"))
        self.sidebar_logo.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.sidebar_logout_btn = ctk.CTkButton(self.sidebar, command=self.sidebar_logout_btn_event)
        self.sidebar_logout_btn.grid(row=1, column=0, padx=20, pady=10)
        
        self.sidebar_exit_btn = ctk.CTkButton(self.sidebar, command=self.sidebar_exit_btn_event)
        self.sidebar_exit_btn.grid(row=2, column=0, padx=20, pady=10)
        
        self.sidebar_set_key_btn = ctk.CTkButton(self.sidebar, command=self.sidebar_set_key_btn_event)
        self.sidebar_set_key_btn.grid(row=3, column=0, padx=20, pady=10)
        
        self.sidebar_change_color_btn = ctk.CTkButton(self.sidebar, command=self.change_output_color_event)
        self.sidebar_change_color_btn.grid(row=4, column=0, padx=20, pady=10, sticky="sw")
        
        #//////////// THEME SELECT ////////////
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        #//////////// UI SIZE SCALING SELECT ////////////
        self.scaling_label = ctk.CTkLabel(self.sidebar, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_option_menu = ctk.CTkOptionMenu(self.sidebar, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_option_menu.grid(row=8, column=0, padx=20, pady=(10, 20))

        #//////////// COMMAND ENTRY ////////////
        self.command_entry = ctk.CTkEntry(self, placeholder_text="Enter a command. Try 'help' for a list of commands.")
        self.command_entry.grid(row=3, column=1, columnspan=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        #//////////// CLEAR BUTTON ////////////
        self.clear_btn = ctk.CTkButton(self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=(self.clearAll), text="Clear")
        self.clear_btn.grid(row=3, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        #//////////// SEND BUTTON ////////////
        self.send_btn = ctk.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("#DCE4EE"), command=(self.process_input), text="Send Query")
        self.send_btn.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

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
        
        #//////////// ENGINE OPTION MENU ////////////
        _gtp_engines = []
        for _index in range(len(self.wingtp_cli.engines)):
            _gtp_engines.append(self.wingtp_cli.engines[_index][0])
            _index += 1

        self.engine_option_menu = ctk.CTkOptionMenu(
            self.gtp_options_tabview.tab("Response"), 
            dynamic_resizing=False, 
            values=_gtp_engines, #["Value 1", "Value 2", "Value 3"]
            command=self.on_engine_option_chosen_event
        )
        self.engine_option_menu.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        #//////////// RESPONSE TOKEN LIMIT INPUT ////////////
        self.response_token_limit_input = ctk.CTkButton(self.gtp_options_tabview.tab("Response"), text="Response Token Limit", command=self.open_response_token_limit_input_dialog_event)
        self.response_token_limit_input.grid(row=1, column=0, padx=20, pady=(10, 10))
        
        #//////////// RESPONSE COUNT INPUT ////////////
        self.response_count_input = ctk.CTkButton(self.gtp_options_tabview.tab("Response"), text="Response Count", command=self.open_response_count_input_dialog_event)
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
        
        # create radiobutton frame
        self.radiobutton_frame = ctk.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
        
        self.label_radio_group = ctk.CTkLabel(master=self.radiobutton_frame, text="Pinned GTP Engines:")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_1 = ctk.CTkRadioButton(master=self.radiobutton_frame, text=self.wingtp_cli.engines[0][0], variable=self.radio_var, value=0)
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="nw")
        self.radio_button_2 = ctk.CTkRadioButton(master=self.radiobutton_frame, text=self.wingtp_cli.engines[3][0], variable=self.radio_var, value=1)
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="nw")
        self.radio_button_3 = ctk.CTkRadioButton(master=self.radiobutton_frame, text=self.wingtp_cli.engine, variable=self.radio_var, value=2)
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="nw")

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

        # create scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="CTkScrollableFrame")
        self.scrollable_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        
        self.scrollable_frame_switches = []
        for i in range(10):
            switch = ctk.CTkSwitch(master=self.scrollable_frame, text=f"CTkSwitch {i}")
            switch.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(switch)

        # create checkbox and switch frame
        self.checkbox_slider_frame = ctk.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
       
        self.checkbox_1 = ctk.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_2 = ctk.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_3 = ctk.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")

        #//////////// DEFAULT VALUES ////////////
        self.sidebar_logout_btn.configure(state="normal", text="Logout")
        self.sidebar_exit_btn.configure(state="normal", text="Exit")
        self.sidebar_set_key_btn.configure(state="normal", text="API Key")
        self.sidebar_change_color_btn.configure(state="normal", text="Color")
        self.checkbox_3.configure(state="disabled")
        self.checkbox_1.select()
        self.scrollable_frame_switches[0].select()
        self.scrollable_frame_switches[4].select()
        self.radio_button_3.configure(state="disabled")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_option_menu.set("100%")
        self.engine_option_menu.set("Engine")
        
        #//////////// GUI METHODS ////////////
    
    def clearAll(self):
        self.clearInput()
        self.clearOutput()
        self.command_entry.delete(0, tk.END)
    
    def on_engine_option_chosen_event(self, engine) -> None:
        self.wingtp_cli.setEngine(f"{engine}")
        self.setOutput(f"Engine changed to: {engine}", "cli")
            
    def open_jsonl_datafile_input_dialog_event(self) -> bool:
        dialog = ctk.CTkInputDialog(text="Enter a .jsonl file path: ", title="JSONL Data File Input")
        path = str(dialog.get_input())
        if path == "None":
            return False
        if len(path) != 0:
            if os.path.exists(path):
                self.wingtp_cli.setJSONLDataFile(path)
                self.setOutput(f"File set: [{self.wingtp_cli.getJSONLDataFile()}]", "cli")
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
                self.wingtp_cli.setUserDefinedFileName(path)
                self.setOutput(f"File set: [{self.wingtp_cli.getUserDefinedFileName()}]", "cli")
                return True
            else:
                self.setOutput(f"File doesn\'t exist! [{path}]", "cli")
                return False
            return False
  
    def open_organization_input_dialog_event(self) -> bool:
        dialog = ctk.CTkInputDialog(text="Enter organization: ", title="Organization Input")
        organization = str(dialog.get_input())
        if len(organization) != 0 and organization != "None":
            self.wingtp_cli.setOrganization(organization)
            self.setOutput(f"Organization changed to: [{self.wingtp_cli.getOrganization()}]", "cli")
            return True
        else:
            return False
        
    def open_api_version_input_dialog_event(self) -> bool:
        dialog = ctk.CTkInputDialog(text="Enter the API version: ", title="API Version Input")
        api_version = str(dialog.get_input())
        if len(api_version) != 0 and api_version != "None":
            self.wingtp_cli.setAPIVersion(api_version)
            self.setOutput(f"API version changed to: [{self.wingtp_cli.getAPIVersion()}]", "cli")
            return True
        else:
            return False
            
    def open_api_type_input_dialog_event(self) -> bool:
        dialog = ctk.CTkInputDialog(text="Enter the API type: ", title="API Type Input")
        api_type = str(dialog.get_input())
        if len(api_type) != 0 and api_type != "None":
            self.wingtp_cli.setAPIType(api_type)
            self.setOutput(f"API type changed to: [{self.wingtp_cli.getAPIType()}]", "cli")
            return True
        else:
            return False

    def open_api_base_input_dialog_event(self) -> bool:
        dialog = ctk.CTkInputDialog(text="Enter the API base: ", title="API Base Input")
        api_base = str(dialog.get_input())
        if len(api_base) != 0 and api_base != "None":
            self.wingtp_cli.setAPIBase(api_base)
            self.setOutput(f"API base changed to: [{self.wingtp_cli.getAPIBase()}]", "cli")
            return True
        else:
            return False

    def open_response_token_limit_input_dialog_event(self) -> bool: 
        dialog = ctk.CTkInputDialog(text="Enter the response token limit: ", title="Response Token Limit Input")
        token_limit = str(dialog.get_input())
        if token_limit.isdigit() and token_limit != "None": # Don't test for 0 because the user may want 0!
            self.wingtp_cli.setResponseTokenLimit(token_limit)
            self.setOutput(f"Response token limit changed to: [{self.wingtp_cli.getResponseTokenLimit()}]", "cli")
            return True
        else:
            return False
        
    def open_response_count_input_dialog_event(self) -> bool:
        dialog = ctk.CTkInputDialog(text="Enter the response count: ", title="Response Count Input")
        response_count = str(dialog.get_input())
        if response_count.isdigit() and response_count != "None":
            self.wingtp_cli.setResponseCount(response_count)
            self.setOutput(f"Response count changed to: [{self.wingtp_cli.getResponseCount()}]", "cli")
            return True
        else:
            return False
        
    def change_appearance_mode_event(self, _new_appearance_mode: str) -> bool:
        _theme = _new_appearance_mode
        if len(_theme) != 0 and _theme != "None":
            ctk.set_appearance_mode(_theme)
            self.setOutput(f"Appearance mode changed to: {_theme}", "cli")
            return True
        else:
            self.setOutput(f"Appearance mode: {_theme} doesn\'t exist!\nOptions are [Light|Dark|System]", "cli")
            return False
            
    def change_output_color_event(self) -> None:
        color = colorchooser.askcolor(title="Select Color")
        self._OUTPUT_COLOR = f"{color[1]}"
        self.output_box.configure(text_color=self._OUTPUT_COLOR)
               
    def change_scaling_event(self, new_scaling: str) -> None:
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def sidebar_logout_btn_event(event) -> None:
        pass
    
    def sidebar_exit_btn_event(self) -> None:
        sys.exit(0)
 
    def sidebar_set_key_btn_event(self) -> None:
        pass
        
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

    def setOutput(self, output: str, type) -> None:
        if type == "chat":
            self.output_box.insert(tk.END, f"\n{self.nt.time(False)} [{self.wingtp_cli.engine}]: {output}\n")
        elif type == "cli":
            self.output_box.insert(tk.END, f"\n{self.nt.time(False)} [wingtp]: {output}\n")
        elif type == "user":
            self.output_box.insert(tk.END, f"\n{self.nt.time(False)} [{self.USER}]: {output}\n")

    def getUsername(self) -> str:
        return self.wingtp_cli.readFile('./config/username.conf')

    def setUsername(self) -> None:
        username = simpledialog.askstring('Enter a username that you would like to use: ')
        self.USER = username

    def processQueryRequest(self, request: str) -> None:
        self.wingtp_cli.setAPIKeyPath(self.API_KEY_PATH)
        self.wingtp_cli.setEngine(self.wingtp_cli.engine)
        self.wingtp_cli.setResponseTokenLimit(self.wingtp_cli.response_token_limit)
        self.wingtp_cli.setResponseCount(self.wingtp_cli.response_count)
        self.wingtp_cli.setRequest(request)
        self.wingtp_cli.requestData()
        response = self.wingtp_cli.getResponse()
        self.clearInput()
        self.setOutput(request, "user")
        self.setOutput(response, "chat")
    
    def processCommandRequest(self, request: str) -> None:
        if request == self.wingtp_cli.cli_options[0]:
            self.setOutput("Goodbye! ...", "cli")
            sys.exit()
        elif request == self.wingtp_cli.cli_options[1]:
            self.open_response_token_limit_input_dialog_event()
            self.clearInput()
        elif request == self.wingtp_cli.cli_options[2]:
            engine = simpledialog.askstring("Input", "Set the engine: ")
            self.wingtp_cli.setEngine(engine)
            self.clearInput()
            self.setOutput(f"Engine set to {self.wingtp_cli.getEngine()}", "cli")
        elif request == self.wingtp_cli.cli_options[3]:
            self.open_response_count_input_dialog_event()
            self.clearInput()
        elif request == self.wingtp_cli.cli_options[4]:
            self.open_api_base_input_dialog_event()
            self.clearInput()
        elif request == self.wingtp_cli.cli_options[5]:
            self.open_api_type_input_dialog_event()
            self.clearInput()
        elif request == self.wingtp_cli.cli_options[6]:
            self.open_api_version_input_dialog_event()
            self.clearInput()
        elif request == self.wingtp_cli.cli_options[7]:
            self.open_organization_input_dialog_event()
            self.clearInput()
        elif request == self.wingtp_cli.cli_options[8]:
            self.open_user_defined_datafile_input_dialog_event()
            self.clearInput()
        elif request == self.wingtp_cli.cli_options[9]:
            self.open_jsonl_datafile_input_dialog_event()
            self.clearInput()
        elif request == self.wingtp_cli.cli_options[10]:
            self.clearInput()
            self.setOutput(self.wingtp_cli._help.__doc__, "cli")
        elif request == self.wingtp_cli.cli_options[11]:
            self.clearOutput()
        elif request.split(' ')[0] == self.wingtp_cli.cli_options[12]:
            self.change_appearance_mode_event(request.split(' ')[1])
        elif request == self.wingtp_cli.cli_options[13]:
            self.change_output_color_event()
        else:
            self.setOutput(self.wingtp_cli._help.__doc__, "cli")
    
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
{self.wingtp_cli._help.__doc__}", "cli")

#//////////// MAIN ENTRY POINT
if __name__ == "__main__":
    wingtp = WinGTPGUI()
    wingtp.setOutput(wingtp.wingtp_cli.greetUser(wingtp.USER, wingtp.API_KEY_PATH), 'chat')
    wingtp.mainloop()
