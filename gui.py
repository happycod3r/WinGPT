import tkinter as tk
from tkinter import font
import customtkinter as ctk 
from win_gtp import WinGTP

# label1 = tk.Label(window, text="Label 1")
# label1.grid(row=0, column=0)

# label2 = tk.Label(window, text="Label 2")
# label2.grid(row=1, column=0)

# button = tk.Button(window, text="Button")
# button.grid(row=1, column=1)

# myapp    - [] x
# Label 1
# Label 2  Button
#////// EVENT HANDLERS //////

def process_input():
    user_input = input_box.get("1.0", tk.END).strip()
    API_KEY_PATH = './.api_key.conf'
    newRequest = WinGTP()
    newRequest.setAPIKeyPath(API_KEY_PATH)  
    newRequest.setResponseTokenLimit(newRequest.response_token_limit)
    newRequest.setEngine(newRequest.engine)
    newRequest.setResponseCount(newRequest.response_count)
    newRequest.setRequest(str(user_input))
    newRequest.requestData()
    response = newRequest.getResponse()
    output_box.insert(tk.END, f"{response}\n")
    
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
    bg_color="#328387",
    text="WinGTP v0.1.0",
    font=title_font,
    #compound="center"
)
title.grid(row=0, column=0, sticky="nsew")
#title.grid_rowconfigure(0, weight=1)

#////// OUTPUT BOX //////
output_box_font = ctk.CTkFont(
    "Segoi UI", 
    size=14
)
output_box = ctk.CTkTextbox(
    wingtp,
    height=420,
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
    size=12
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
input_box.grid(row=2, column=0, sticky="nsew", padx=2, pady=2)
#input_box.grid_rowconfigure(2, weight=1)

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
send_btn.grid(row=3, column=0, sticky="nsew")
#send_btn.grid_rowconfigure(3, weight=1)

#////// SYSTEM SETTINGS //////
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

#////// WINDOW //////
wingtp.title("WinGTP Powered by Python & OpenAI")
wingtp.geometry('700x750')
wingtp.grid_columnconfigure(0, weight=1)
wingtp.grid_rowconfigure(0, weight=1)

print(wingtp.grid_size())
wingtp.mainloop()
