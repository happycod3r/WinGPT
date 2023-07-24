import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import persistence


class ImageForm(ctk.CTkFrame):
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
        
        self.title = ctk.CTkLabel(self, text="Images")
        self.title.grid(row=0, column=0, sticky="ew", padx=10, pady=0)
        
        self.size_menu = ctk.CTkOptionMenu(
            self, 
            dynamic_resizing=False, 
            values=["256x256", "512x512", "1024x1024"],
            command=self.onImageSizeSelected
        )
        self.size_menu.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        
        self.path_label = ctk.CTkLabel(self, text="Path:")
        self.path_label.grid(row=2, column=0, sticky="ew", padx=10, pady=0)
        
        self.chosen_img_path_label = ctk.CTkEntry(self, border_width=0, corner_radius=0, fg_color="#333333", placeholder_text="")
        self.chosen_img_path_label.grid(row=3, column=0, sticky="ew", padx=10, pady=0)
        
        self.choose_img_btn = ctk.CTkButton(self, text="Choose an Image", command=self.onChooseImageBtnClicked)
        self.choose_img_btn.grid(row=4, column=0, columnspan=1, sticky="ew", padx=10, pady=0)
        
        self.chosen_img_mask_path_label = ctk.CTkEntry(self, border_width=0, corner_radius=0, fg_color="#333333", placeholder_text="")
        self.chosen_img_mask_path_label.grid(row=5, column=0, sticky="ew", padx=10, pady=0)
        
        self.choose_img_mask_btn = ctk.CTkButton(self, text="Choose a Mask", command=self.onChooseImageMaskBtnClicked)
        self.choose_img_mask_btn.grid(row=6, column=0, columnspan=1, sticky="ew", padx=10, pady=0)
    
    def openFileDialog(self) -> (str | bool):
        file_path = filedialog.askopenfilename()
        if file_path:
            return file_path
        else:
            return False

    def onChooseImageBtnClicked(self) -> False:
        _path = self.openFileDialog()
        if _path == False:
            return False
        self.chosen_img_path_label.configure(placeholder_text=f"{_path}")

        self._config.openConfig()
        self._config.setOption("image_requests", "img_path", _path)
        self._config.saveConfig()
        
    def onChooseImageMaskBtnClicked(self) -> False:
        _path = self.openFileDialog()
        if _path == False:
            return False
        self.chosen_img_mask_path_label.configure(placeholder_text=f"{_path}")

        self._config.openConfig()
        self._config.setOption("image_requests", "mask_path", _path)
        self._config.saveConfig()

    def onImageSizeSelected(self, _size: str) -> None:
        self._config.openConfig()
        self._config.setOption("image_requests", "img_size", f"{_size}")
        self._config.saveConfig()
