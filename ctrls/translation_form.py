import customtkinter as ctk
import iso639

class CustomTkTextbox(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(
            padx=30, 
            pady=30,
            border_width=1,
            corner_radius=6
        )  # Set the inner padding values
        
        self.lang1_option_menu = ctk.CTkOptionMenu(
            self, 
            dynamic_resizing=False, 
            values=self.getLanguages(),
            command=self.on_language1_option_selected
        )
        
        self.lang2_option_menu = ctk.CTkOptionMenu(
            self, 
            dynamic_resizing=False, 
            values=self.getLanguages(),
            command=self.on_language2_option_selected
        )
    
        
    def getLanguages(self) -> list:
        pass

    def on_language1_option_selected(self, lang1: str) -> None:
        pass
    
    def on_language2_option_selected(self, lang2: str) -> None:
        pass
