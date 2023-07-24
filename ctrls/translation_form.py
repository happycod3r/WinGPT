import customtkinter as ctk
import iso639
import modules.persistence as persistence

class TranslationsForm(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(
            bg_color="transparent",
            border_width=0,
            corner_radius=6,
        )
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
        
        self._config = persistence.Persistence()
        self.langs = iso639.data
        self.LANG1 = None
        self.LANG2 = None
        
        self.title = ctk.CTkLabel(self, text="Translations", anchor="center")
        self.title.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        
        self.from_label = ctk.CTkLabel(self, text="From: ")
        self.from_label.grid(row=1, column=0, sticky="ew")
        
        self.lang1_option_menu = ctk.CTkOptionMenu(
            self, 
            dynamic_resizing=False, 
            values=self.getLanguages(),
            command=self.on_language1_option_selected
        )
        self.lang1_option_menu.grid(row=1, column=1)
        
        self.to_label = ctk.CTkLabel(self, text="To: ")
        self.to_label.grid(row=2, column=0, sticky="ew")
        
        self.lang2_option_menu = ctk.CTkOptionMenu(
            self, 
            dynamic_resizing=False, 
            values=self.getLanguages(),
            command=self.on_language2_option_selected
        )
        self.lang2_option_menu.grid(row=2, column=1)
        
    def getLanguages(self) -> list:
        lang_names = []
        for i in range(len(self.langs)):
            lang_names.append(self.langs[i]["name"])
        return lang_names

    def on_language1_option_selected(self, _lang1: str) -> None:
        self.LANG1 = _lang1
        self._config.openConfig()
        self._config.setOption("translations", "lang1", f"{self.LANG1}")
        self._config.saveConfig()
    
    def on_language2_option_selected(self, _lang2: str) -> None:
        self.LANG2 = _lang2
        self._config.openConfig()
        self._config.setOption("translations", "lang2", f"{self.LANG2}")
        self._config.saveConfig()
