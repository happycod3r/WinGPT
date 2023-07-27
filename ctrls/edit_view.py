import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import os
import modules.persistence as persistence
import cli
import modules.stdops as stdops

class EditView(ctk.CTkScrollableFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cli = cli.OpenAIInterface()
        self.stdops = stdops.StdOps()
    
        self.file_path = None
        
        self.configure(
            bg_color="transparent",
            border_width=0,
            corner_radius=6,
        )
        
        self.grid_rowconfigure((0, 1, 2, 3), weight=0)
        self.grid_columnconfigure(0, weight=0)
    
        self.title_label = ctk.CTkLabel(self, text="Edits", anchor="center")
        self.title_label.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
        self.title_label.grid_rowconfigure(0, weight=0)   
        
        self.edit_type_menu = ctk.CTkOptionMenu(
            self, 
            values=[
                "Fix the spelling mistakes",
                "Fix the capitalization mistakes", 
                "Fix the punctuation mistakes",
                "Fix all mistakes",
                "Convert all text to lower case",
                "Convert all text to upper case"
                ],
            command=self.onEditTypeSelected
        )
        self.edit_type_menu.grid(row=1, column=0, sticky="ew", padx=10, pady=(10, 0))
        self.edit_type_menu.grid_rowconfigure(0, weight=0)
           
    def onEditTypeSelected(self, type):
        edit_type=self.edit_type_menu.get()
        self.cli.setInstruction(edit_type)

    
    def openFileDialog(self) -> (str | bool):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.cli.setAudioFile(file_path)
            self.file_path
            return file_path
        else:
            return False            
