import tkinter as tk
import customtkinter as ctk
from tkinter import simpledialog
import tkinter.messagebox
from tkinter import *
from bin import normaltime
from chatmemory import memory
from wingtpcli import WinGTPCLI
from ctrls import ctktextbox
import sys
import os 

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class WinGTPGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        #//////////// WINGTP GUI PROPERTIES
        self.USER = 'paul'
        self.API_KEY_PATH = './config/.api_key.conf'
        self.wingtp_cli = WinGTPCLI()
        self.nt = normaltime.NormalTime()
        
        #//////////// WINDOW
        self.title("WinGTP Powered by Python & OpenAI")
        self.geometry(f"{1100}x{580}")

        #//////////// GRID LAYOUT (4x4) ////////////
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        #//////////// IMAGES ////////////

        #//////////// SIDEBAR ////////////
        self.sidebar = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)
        
        #//////////// SIDEBAR LOGO ////////////
        self.sidebar_logo = ctk.CTkLabel(self.sidebar, text="WinGTP v0.1.0", font=ctk.CTkFont(size=20, weight="bold"))
        self.sidebar_logo.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.sidebar_button_1 = ctk.CTkButton(self.sidebar, command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        
        self.sidebar_button_2 = ctk.CTkButton(self.sidebar, command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        
        self.sidebar_button_3 = ctk.CTkButton(self.sidebar, command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        self.scaling_label = ctk.CTkLabel(self.sidebar, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_option_menu = ctk.CTkOptionMenu(self.sidebar, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_option_menu.grid(row=8, column=0, padx=20, pady=(10, 20))

        #//////////// COMMAND ENTRY ////////////
        self.command_entry = ctk.CTkEntry(self, placeholder_text="Enter a command. Try 'help' for a list of commands.")
        self.command_entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        #//////////// SEND BUTTON ////////////
        self.send_btn = ctk.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=(self.process_input), text="Send Query")
        self.send_btn.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        #//////////// OUTPUT BOX ////////////
        self.output_box = ctk.CTkTextbox(self, width=250, font=ctk.CTkFont(size=14, weight='bold'))
        self.output_box.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
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
            values=_gtp_engines #["Value 1", "Value 2", "Value 3"]
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
        self.organization_input = ctk.CTkButton(self.gtp_options_tabview.tab("API"), text="Organization", command=self.open_organization_input_dialog_event)
        self.organization_input.grid(row=3, column=0, padx=20, pady=(10, 10))
        
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # create radiobutton frame
        self.radiobutton_frame = ctk.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = ctk.CTkLabel(master=self.radiobutton_frame, text="CTkRadioButton Group:")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_1 = ctk.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=0)
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_2 = ctk.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=1)
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_3 = ctk.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=2)
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

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
        self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        self.checkbox_3.configure(state="disabled")
        self.checkbox_1.select()
        self.scrollable_frame_switches[0].select()
        self.scrollable_frame_switches[4].select()
        self.radio_button_3.configure(state="disabled")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_option_menu.set("100%")
        self.engine_option_menu.set("Engine")
        
        #//////////// GUI METHODS ////////////

    def open_organization_input_dialog_event(self):
        pass

    def open_api_version_input_dialog_event(self):
        dialog = ctk.CTkInputDialog(text="Enter the API version: ", title="API Version Input")
        self.wingtp_cli.setAPIVersion(str(dialog.get_input()))
        self.setOutput(f"API version change to: [{self.wingtp_cli.getAPIVersion()}]", "cli")

    def open_api_type_input_dialog_event(self):
        dialog = ctk.CTkInputDialog(text="Enter the API type: ", title="API Type Input")
        self.wingtp_cli.setAPIType(str(dialog.get_input()))
        self.setOutput(f"API type change to: [{self.wingtp_cli.getAPIType()}]", "cli")

    def open_api_base_input_dialog_event(self):
        dialog = ctk.CTkInputDialog(text="Enter the API base: ", title="API Base Input")
        self.wingtp_cli.setAPIBase(str(dialog.get_input()))
        self.setOutput(f"API base change to: [{self.wingtp_cli.getAPIBase()}]", "cli")

    def open_response_token_limit_input_dialog_event(self):
        dialog = ctk.CTkInputDialog(text="Enter the response token limit: ", title="Response Token Limit Input")
        self.wingtp_cli.setResponseTokenLimit(int(dialog.get_input()))
        self.setOutput(f"Response token limit changed to: [{self.wingtp_cli.getResponseTokenLimit()}]", "cli")
        
    def open_response_count_input_dialog_event(self):
        dialog = ctk.CTkInputDialog(text="Enter the response count: ", title="Response Count Input")
        self.wingtp_cli.setResponseCount(int(dialog.get_input()))
        self.setOutput(f"Response count changed to: [{self.wingtp_cli.getResponseCount()}]", "cli")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")
 
    def clearInput(self) -> None:
        self.input_box.delete("1.0", tk.END)
    
    def clearOutput(self) -> None:
        self.output_box.delete("1.0", tk.END)
        self.clearInput()
    
    def getUserInput(self) -> str:
        user_input = self.input_box.get("1.0", tk.END).strip()
        return str(user_input)

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

    def process_input(self) -> None:
        request = self.getUserInput()

        if request == self.wingtp_cli.cli_options[0]:
            self.setOutput('Goodbye! ...', 'cli')
            sys.exit()
        elif request == self.wingtp_cli.cli_options[1]:
            token_limit = simpledialog.askinteger('Input', 'Set the max amount of reponse tokens: ')
            self.wingtp_cli.setResponseTokenLimit(int(token_limit))
            self.clearInput()
            self.setOutput(f'Token limit set to {self.wingtp_cli.getResponseTokenLimit()} tokens per response.', 'cli')
        elif request == self.wingtp_cli.cli_options[2]:
            engine = simpledialog.askstring('Input', 'Set the engine: ')
            self.wingtp_cli.setEngine(engine)
            self.clearInput()
            self.setOutput(f'Engine set to {self.wingtp_cli.getEngine()}', 'cli')
        elif request == self.wingtp_cli.cli_options[3]:
            response_count = simpledialog.askinteger('Input', 'Set the number of reponses: ')
            self.wingtp_cli.setResponseCount(int(response_count))
            self.clearInput()
            self.setOutput(f'The number of reponses is set to {self.wingtp_cli.getResponseCount()}', 'cli')
        elif request == self.wingtp_cli.cli_options[4]:
            api_base = simpledialog.askstring('Input', 'Set the API base: ')
            self.wingtp_cli.setAPIBase(str(api_base))
            self.clearInput()
            self.setOutput(f'The API base is set to {self.wingtp_cli.getAPIBase()}', 'cli')
        elif request == self.wingtp_cli.cli_options[5]:
            api_type = simpledialog.askstring('Input', 'Set the API type: ')
            self.wingtp_cli.setAPIType(str(api_type))
            self.clearInput()
            self.setOutput(f'The API type is set to {self.wingtp_cli.getAPIType()}', 'cli')
        elif request == self.wingtp_cli.cli_options[6]:
            api_version = simpledialog.askstring('Input', 'Set the API version: ')
            self.wingtp_cli.setAPIVersion(str(api_version))
            self.clearInput()
            self.setOutput(f'The API version is set to {self.wingtp_cli.getAPIVersion()}', 'cli')
        elif request == self.wingtp_cli.cli_options[7]:
            organization = simpledialog.askstring('Input', 'Set the organization name: ')
            self.wingtp_cli.setOrganization(str(organization))
            self.clearInput()
            self.setOutput(f'The API base is set to {self.wingtp_cli.getOrganization()}', 'cli')
        elif request == self.wingtp_cli.cli_options[8]:
            user_defined_filename = simpledialog.askstring('Input', 'Set a user defined file name: ')
            self.wingtp_cli.setUserDefinedFileName(str(user_defined_filename))
            self.clearInput()
            self.setOutput(f'The user defined file name is set to {self.wingtp_cli.getUserDefinedFileName()}', 'cli')
        elif request == self.wingtp_cli.cli_options[9]:
            jsonl_file_path = simpledialog.askstring('Input', 'Set a JSONL file: ')
            self.wingtp_cli.setJSONLDataFile(str(jsonl_file_path))
            self.clearInput()
            self.setOutput(f'The JSONL file is set to {self.wingtp_cli.getJSONLDataFile()}', 'cli')
        elif request == self.wingtp_cli.cli_options[10]:
            self.clearInput()
            self.setOutput(self.wingtp_cli._help.__doc__, 'cli')
        elif request == self.wingtp_cli.cli_options[11]:
            self.clearOutput()
        else:
            self.wingtp_cli.setAPIKeyPath(self.API_KEY_PATH)
            self.wingtp_cli.setEngine(self.wingtp_cli.engine)
            self.wingtp_cli.setResponseTokenLimit(self.wingtp_cli.response_token_limit)
            self.wingtp_cli.setResponseCount(self.wingtp_cli.response_count)
            self.wingtp_cli.setRequest(request)
            self.wingtp_cli.requestData()
            response = self.wingtp_cli.getResponse()
            self.clearInput()
            self.setOutput(request, 'user')
            self.setOutput(response, 'chat')
            
#//////////// MAIN ENTRY POINT
if __name__ == "__main__":
    wingtp = WinGTPGUI()
    wingtp.setOutput(wingtp.wingtp_cli.greetUser(wingtp.USER, wingtp.API_KEY_PATH), 'chat')
    wingtp.mainloop()
