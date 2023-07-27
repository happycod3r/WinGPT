import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import os
import modules.persistence as persistence
import cli
import modules.stdops as stdops

class AudioTranscriptionView(ctk.CTkScrollableFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cli = cli.OpenAIInterface()
        self.stdops = stdops.StdOps()
        self.CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
        self.TMP_EMBEDDINGS_FILE = f"{self.CURRENT_PATH}\\..\\tmp\\embedding.tmp" 
        self.audio_file_path = None
        
        self.configure(
            bg_color="transparent",
            border_width=0,
            corner_radius=6,
        )
        
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.grid_columnconfigure(0, weight=0)
    
        self.title_label = ctk.CTkLabel(self, text="Audio Transcription", anchor="center")
        self.title_label.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
        self.title_label.grid_rowconfigure(0, weight=1)
        
        self.file_path_output = ctk.CTkEntry(self, border_width=0)
        self.file_path_output.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        self.file_path_output.grid_rowconfigure(1, weight=0)
        
        self.choose_audio_file_btn = ctk.CTkButton(self, text="Choose Audio File", command=self.openFileDialog)
        self.choose_audio_file_btn.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        self.choose_audio_file_btn.grid_rowconfigure(2, weight=0)
        
        self.transcribe_btn = ctk.CTkButton(self, text="Transcribe", command=self.transcribe)
        self.transcribe_btn.grid(row=3, column=0, sticky="ew", padx=10, pady=10)
        self.transcribe_btn.grid_rowconfigure(3, weight=0)
        
        self.copy_transcript_btn = ctk.CTkButton(self, text="Copy Transcript", command=self.copyTranscript)
        self.copy_transcript_btn.grid(row=4, column=0, sticky="ew", padx=10, pady=10)
        self.copy_transcript_btn.grid_rowconfigure(4, weight=0)
        
        self.transcript_output = ctk.CTkTextbox(self, border_width=0)
        self.transcript_output.grid(row=5, column=0, sticky="ew", padx=0, pady=(0, 10)) 
        self.transcript_output.grid_rowconfigure(5, weight=0)     
    
    def transcribe(self):
        self.cli.requestData()
        response = self.cli.getTranscriptResponse()
        self.transcript_output.insert("1.0", text=f"{response}")

    def copyTranscript(self):
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
     
    def openFileDialog(self) -> (str | bool):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.cli.setAudioFile(file_path)
            self.audio_file_path = file_path
            self.file_path_output.insert(0, file_path)
            return file_path
        else:
            return False            
