import tkinter as tk
import customtkinter as ctk 
from win_gtp import WinGTP

USER = 'paul'

def clearInput():
    input_box.delete("1.0", tk.END)
    #small_input_box.delete("1.0", tk.END)
    
def getUserInput():
    user_input = input_box.get("1.0", tk.END).strip()
    return user_input

def process_input():
    API_KEY_PATH = './.api_key.conf'
    request = str(getUserInput())
    newRequest = WinGTP()
    newRequest.setAPIKeyPath(API_KEY_PATH)  
    newRequest.setResponseTokenLimit(newRequest.response_token_limit)
    newRequest.setEngine(newRequest.engine)
    newRequest.setResponseCount(newRequest.response_count)
    newRequest.setRequest(request)
    newRequest.requestData()
    
    clearInput()
    
    response = newRequest.getResponse()
    setOutput(f"[{USER}]: {request}\n")

    setOutput(f"[{newRequest.engine}]: {response}\n")
    
def setOutput(output):
    output_box.insert(tk.END, f"{output}\n")
    
#////// GUI //////
wingtp = ctk.CTk()

title_font = ctk.CTkFont(
    "Segoi UI", 
    size=16
)
title = ctk.CTkLabel(
    wingtp,
    height=40,
    corner_radius=0,
    bg_color="#0077b6",
    text="WinGTP v0.1.0",
    font=title_font,
    #compound="center"
)
title.grid(row=0, column=0, sticky="nsew")
title.grid_rowconfigure(0, weight=1)

#////// OUTPUT BOX //////
output_box_font = ctk.CTkFont(
    "Segoi UI", 
    size=16
)
output_box = ctk.CTkTextbox(
    wingtp,
    height=380,
    corner_radius=0,
    border_width=0,
    text_color="#e2e2e2",
    font=output_box_font,
    
)
output_box.grid(row=1, column=0, sticky="nsew")
output_box.grid_rowconfigure(1)
output_box.grid_columnconfigure(0, weight=1)

#////// INPUT BOX //////
input_box_font = ctk.CTkFont(
    "Segoi UI", 
    size=16
)
input_box = ctk.CTkTextbox(
    wingtp,
    height=240,
    corner_radius=0,
    border_width=1,
    border_color="#6d6d6d",
    text_color="#e2e2e2",
    font=input_box_font,
)
input_box.grid(row=2, column=0, sticky="nsew")

#////// SMALL INPUT BOX //////
small_input_box_font = ctk.CTkFont(
    "Segoi UI", 
    size=16
)
small_input_box = ctk.CTkEntry(
    wingtp,
    height=40,
    corner_radius=0,
    border_width=1,
    border_color="#6d6d6d",
    text_color="#e2e2e2",
    font=small_input_box_font,
    placeholder_text="Start chatting..."
)
small_input_box.grid(row=3, column=0, sticky="nsew")

#////// SEND BUTTON //////
send_btn_font = ctk.CTkFont(
    "Segoi UI",
    size=16
)
send_btn = ctk.CTkButton(
    wingtp,
    height=40,
    corner_radius=0,
    border_width=0,
    font=send_btn_font,
    text="Send Query",
    text_color="#e2e2e2",
    command=(process_input)
)
send_btn.grid(row=4, column=0, sticky="nsew")

#////// SYSTEM SETTINGS //////
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

#////// WINDOW //////
wingtp.title("WinGTP Powered by Python & OpenAI")
wingtp.geometry('700x750')
wingtp.grid_columnconfigure(0, weight=1)
wingtp.grid_rowconfigure(0, weight=1)


wingtp.mainloop()
