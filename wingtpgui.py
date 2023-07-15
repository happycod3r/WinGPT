import sys
from bin import normaltime
import tkinter as tk
import customtkinter as ctk 
from tkinter import simpledialog
from chatmemory import memory
from wingtpcli import WinGTPCLI

#////// GLOBAL VARIABLES ///////////////////////////////////////////////////
USER = 'paul'
API_KEY_PATH = './.api_key.conf'
wingtp_cli = WinGTPCLI()

def clearInput() -> None:
    input_box.delete("1.0", tk.END)
    #small_input_box.delete("1.0", tk.END)
    
def clearOutput():
    output_box.delete("1.0", tk.END)
    clearInput()
    
def getUserInput() -> str:
    user_input = input_box.get("1.0", tk.END).strip()
    return str(user_input)

def setOutput(output: str, type) -> None:
    nt = normaltime.NormalTime()
    if type == "chat":
        output_box.insert(tk.END, f"\n{nt.time(False)} [{wingtp_cli.engine}]: {output}\n")
    elif type == "cli":
        output_box.insert(tk.END, f"\n{nt.time(False)} [wingtp]: {output}\n")
    elif type == "user":
        output_box.insert(tk.END, f"\n{nt.time(False)} [{USER}]: {output}\n")

def getUsername() -> str:
    return USER

def setUsername() -> None:
    username = simpledialog.askstring('Enter a username that you would like to use: ')
    USER = username
    simpledialog.askstring('Input', 'hello')
    
def process_input() -> None:
    request = getUserInput()

    #////////////////////////////////
    if request == wingtp_cli.cli_options[0]:
        setOutput('Goodbye! ...', 'cli')
        sys.exit()
    elif request == wingtp_cli.cli_options[1]:
        token_limit = simpledialog.askinteger('Input', 'Set the max amount of reponse tokens: ')
        wingtp_cli.setResponseTokenLimit(int(token_limit))
        clearInput()
        setOutput(f'Token limit set to {wingtp_cli.getResponseTokenLimit()} tokens per response.', 'cli')
    elif request == wingtp_cli.cli_options[2]:
        engine = simpledialog.askstring('Input', 'Set the engine: ')
        wingtp_cli.setEngine(engine)
        clearInput()
        setOutput(f'Engine set to {wingtp_cli.getEngine()}', 'cli')
    elif request == wingtp_cli.cli_options[3]:
        response_count = simpledialog.askinteger('Input', 'Set the number of reponses: ')
        wingtp_cli.setResponseCount(int(response_count))
        clearInput()
        setOutput(f'The number of reponses is set to {wingtp_cli.getResponseCount()}', 'cli')
    elif request == wingtp_cli.cli_options[4]:
        api_base = simpledialog.askstring('Input', 'Set the API base: ')
        wingtp_cli.setAPIBase(str(api_base))
        clearInput()
        setOutput(f'The API base is set to {wingtp_cli.getAPIBase()}', 'cli')
    elif request == wingtp_cli.cli_options[5]:
        api_type = simpledialog.askstring('Input', 'Set the API type: ')
        wingtp_cli.setAPIType(str(api_type))
        clearInput()
        setOutput(f'The API type is set to {wingtp_cli.getAPIType()}', 'cli')
    elif request == wingtp_cli.cli_options[6]:
        api_version = simpledialog.askstring('Input', 'Set the API version: ')
        wingtp_cli.setAPIVersion(str(api_version))
        clearInput()
        setOutput(f'The API version is set to {wingtp_cli.getAPIVersion()}', 'cli')
    elif request == wingtp_cli.cli_options[7]:
        organization = simpledialog.askstring('Input', 'Set the organization name: ')
        wingtp_cli.setOrganization(str(organization))
        clearInput()
        setOutput(f'The API base is set to {wingtp_cli.getOrganization()}', 'cli')
    elif request == wingtp_cli.cli_options[8]:
        user_defined_filename = simpledialog.askstring('Input', 'Set a user defined file name: ')
        wingtp_cli.setUserDefinedFileName(str(user_defined_filename))
        clearInput()
        setOutput(f'The user defined file name is set to {wingtp_cli.getUserDefinedFileName()}', 'cli')
    elif request == wingtp_cli.cli_options[9]:
        jsonl_file_path = simpledialog.askstring('Input', 'Set a JSONL file: ')
        wingtp_cli.setJSONLDataFile(str(jsonl_file_path))
        clearInput()
        setOutput(f'The JSONL file is set to {wingtp_cli.getJSONLDataFile()}', 'cli')
    elif request == wingtp_cli.cli_options[10]:
        clearInput()
        setOutput(wingtp_cli._help.__doc__, 'cli')
    elif request == wingtp_cli.cli_options[11]:
        clearOutput()
    else:
        wingtp_cli.setAPIKeyPath(API_KEY_PATH)
        wingtp_cli.setEngine(wingtp_cli.engine)
        wingtp_cli.setResponseTokenLimit(wingtp_cli.response_token_limit)
        wingtp_cli.setResponseCount(wingtp_cli.response_count)
        wingtp_cli.setRequest(request)
        wingtp_cli.requestData()
        response = wingtp_cli.getResponse()
        clearInput()
        setOutput(request, 'user')
        setOutput(response, 'chat')
    
#////////////////////////////////////////////////////////////////////////////
wingtp_gui = ctk.CTk()

title_font = ctk.CTkFont(
    'Segoi UI', 
    size=16
)
title = ctk.CTkLabel(
    wingtp_gui,
    height=40,
    corner_radius=0,
    bg_color='#0077b6',
    text='WinGTP v0.1.0',
    font=title_font,
    #compound="center"
)
title.grid(row=0, column=0, sticky='nsew')
title.grid_rowconfigure(0, weight=1)

#////// OUTPUT BOX //////
output_box_font = ctk.CTkFont(
    'Segoi UI', 
    size=16
)
output_box = ctk.CTkTextbox(
    wingtp_gui,
    height=380,
    corner_radius=0,
    border_width=0,
    text_color='#e2e2e2',
    font=output_box_font,
    
)
output_box.grid(row=1, column=0, sticky='nsew')
output_box.grid_rowconfigure(1)
output_box.grid_columnconfigure(0, weight=1)

#////// INPUT BOX //////
input_box_font = ctk.CTkFont(
    'Segoi UI', 
    size=16
)
input_box = ctk.CTkTextbox(
    wingtp_gui,
    height=240,
    corner_radius=0,
    border_width=1,
    border_color='#6d6d6d',
    text_color='#e2e2e2',
    font=input_box_font,
)
input_box.grid(row=2, column=0, sticky='nsew')

#////// SMALL INPUT BOX //////
small_input_box_font = ctk.CTkFont(
    'Segoi UI', 
    size=16
)
small_input_box = ctk.CTkEntry(
    wingtp_gui,
    height=40,
    corner_radius=0,
    border_width=1,
    border_color='#6d6d6d',
    text_color='#e2e2e2',
    font=small_input_box_font,
    placeholder_text='Start chatting...'
)
small_input_box.grid(row=3, column=0, sticky='nsew')

#////// SEND BUTTON //////
send_btn_font = ctk.CTkFont(
    'Segoi UI',
    size=16
)
send_btn = ctk.CTkButton(
    wingtp_gui,
    height=40,
    corner_radius=0,
    border_width=0,
    font=send_btn_font,
    text='Send Query',
    text_color='#e2e2e2',
    command=(process_input)
)
send_btn.grid(row=4, column=0, sticky='nsew')

#////// SYSTEM SETTINGS //////
ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')

#////// WINDOW //////
wingtp_gui.title('WinGTP Powered by Python & OpenAI')
wingtp_gui.geometry('700x750')
wingtp_gui.grid_columnconfigure(0, weight=1)
wingtp_gui.grid_rowconfigure(0, weight=1)

setOutput(wingtp_cli.greetUser(USER, API_KEY_PATH), 'chat')

wingtp_gui.mainloop()
