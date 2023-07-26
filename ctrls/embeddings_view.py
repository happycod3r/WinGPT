import tkinter as tk
import customtkinter as ctk
import os
import modules.persistence as persistence
import cli
import modules.stdops as stdops

class EmbeddingsView(ctk.CTkScrollableFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cli = cli.OpenAIInterface()
        self.stdops = stdops.StdOps()
        self.CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
        self.TMP_EMBEDDINGS_FILE = f"{self.CURRENT_PATH}\\..\\tmp\\embedding.tmp" 
        
        self.configure(
            bg_color="transparent",
            border_width=0,
            corner_radius=6,
        )
        
        self.grid_rowconfigure((0, 1, 2, 3), weight=0)
        self.grid_columnconfigure(0, weight=0)
    
        self.object_label = ctk.CTkLabel(self, text="embedding", anchor="center")
        self.object_label.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
        self.object_label.grid_rowconfigure(0, weight=0)
        
        self.object_output = ctk.CTkTextbox(self, border_width=0)
        self.object_output.grid(row=1, column=0, sticky="ew", padx=0, pady=(0, 10)) 
        self.object_output.grid_rowconfigure(1, weight=0)
        
        self.show_current_embed_btn = ctk.CTkButton(self, text="Show Latest Embed", command=self.loadEmbedding)
        self.show_current_embed_btn.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        self.show_current_embed_btn.grid_rowconfigure(2, weight=0)
        
        self.copy_embed_btn = ctk.CTkButton(self, text="Copy Embed", command=self.copyEmbedding)
        self.copy_embed_btn.grid(row=3, column=0, sticky="ew", padx=10, pady=10)
        self.copy_embed_btn.grid_rowconfigure(3, weight=0) 

        
        self.loadEmbedding()
        
    def copyEmbedding(self):
        try:
            selected_text = self.object_output.get("1.0", tk.END)
            self.clipboard_clear()
            self.clipboard_append(selected_text)
        except Exception as e:
            print(repr(e))
        
        # I have to clear the file after it's been copied so that it doesn't
        # completely bug out on the next start up. The lag is horendously high
        # during startup trying to load the embedding into the textbox. I 
        # assume it's just too large, so I need to find away to remedy that 
        # because ultimately this is a bad approach as the user may not want to
        # lose that data even if they did copy it. For now though this works.
        # Lag is just that bad.
        self.stdops.writeTofile(self.TMP_EMBEDDINGS_FILE, " ")
                
            
            

    
    def loadEmbedding(self):
        _embed = self.stdops.readFromFile(self.TMP_EMBEDDINGS_FILE)
        if _embed is not False or _embed is not None: 
            self.embed_obj = _embed 
        else:
            self.embed_obj = "No embedding to show\nType something into the input box then press 'Send' to get the embed.\n Once done, press the 'Refresh' button below to see it."
        self.object_output.insert("1.0", text=f"{self.embed_obj}")
