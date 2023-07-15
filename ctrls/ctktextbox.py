import tkinter as tk
import customtkinter as ctk 

class CustomTkTextbox(ctk.CTkTextbox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(
            padx=30, 
            pady=30,
            relief=tk.FLAT
        )  # Set the inner padding values
