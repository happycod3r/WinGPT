import customtkinter
from PIL import Image
import os

customtkinter.set_appearance_mode("dark")


class SetupForm(customtkinter.CTk):
    width = 900
    height = 600

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.USERNAME = None
        self.API_KEY = None
        self.title("Wingtp & OpenAI Setup")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        # load and create background image
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.bg_image = customtkinter.CTkImage(Image.open(current_path + "/images/bg_gradient.jpg"),
                                               size=(self.width, self.height))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        self.setup_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.setup_frame.grid(row=0, column=0, sticky="ns")
        
        self.setup_label = customtkinter.CTkLabel(self.setup_frame, text="WinGTP Setup", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.setup_label.grid(row=0, column=0, padx=30, pady=(150, 15))
        
        self.username_entry = customtkinter.CTkEntry(self.setup_frame, width=200, placeholder_text="username")
        self.username_entry.grid(row=1, column=0, padx=30, pady=(15, 15))
        
        self.api_key_entry = customtkinter.CTkEntry(self.setup_frame, width=200, show="*", placeholder_text="api key")
        self.api_key_entry.grid(row=2, column=0, padx=30, pady=(0, 15))
        
        self.setup_done_button = customtkinter.CTkButton(self.setup_frame, text="Finish Setup", command=self.setup_done_event, width=200)
        self.setup_done_button.grid(row=3, column=0, padx=30, pady=(15, 15))

    def setup_done_event(self):
        self.USERNAME = self.username_entry.get()
        self.API_KEY = self.api_key_entry.get()
        self.destroy()

