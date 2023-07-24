import tkinter as tk
import customtkinter as ctk
import persistence

class QAForm(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(
            bg_color="transparent",
            border_width=0,
            corner_radius=6,
        )
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self._config = persistence.Persistence()
        
        self.title = ctk.CTkLabel(self, text="Questions & Answers")
        self.title.grid(row=0, column=0, sticky="ew", padx=10, pady=0)
        
        self.context_label = ctk.CTkLabel(self, text="Context:")
        self.context_label.grid(row=2, column=0, sticky="ew", padx=10, pady=0)
        
        self.entered_context_label = ctk.CTkEntry(self, border_width=0, corner_radius=0, fg_color="#333333", placeholder_text="")
        self.entered_context_label.grid(row=3, column=0, sticky="ew", padx=10, pady=0)
        
        self.context_entry = ctk.CTkEntry(self, placeholder_text="Enter a question context here.")
        self.context_entry.grid(row=4, column=0, sticky="ew", padx=10, pady=0)
        
        self.enter_context_btn = ctk.CTkButton(self, text="Use Context", command=self.onEnterContextBtnClicked)
        self.enter_context_btn.grid(row=5, column=0, columnspan=1, sticky="ew", padx=10, pady=0)
    
    def onEnterContextBtnClicked(self):
        _context = self.context_entry.get()
        self.context_entry.delete(0, tk.END)
        self.entered_context_label.configure(placeholder_text=f"{_context}")
        self._config.openConfig()
        self._config.setOption("qa", "context_1", _context)
        self._config.saveConfig()
         
    # def on_language2_option_selected(self, _lang2: str) -> None:
    #     self.LANG2 = _lang2
    #     self._config.openConfig()
    #     self._config.setOption("translations", "lang2", f"{self.LANG2}")
    #     self._config.saveConfig()
