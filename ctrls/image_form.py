import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import requests
from io import BytesIO
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
        self.title.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=0)
        
        self.size_menu = ctk.CTkOptionMenu(
            self, 
            dynamic_resizing=False, 
            values=["256x256", "512x512", "1024x1024"],
            command=self.onImageSizeSelected
        )
        self.size_menu.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        
        self.show_img_btn = ctk.CTkButton(self, text="Show", state="disabled", command=self.showImage, width=60)
        self.show_img_btn.grid(row=1, column=1, sticky="ew", padx=10, pady=10)
        
        self.path_label = ctk.CTkLabel(self, text="Path:")
        self.path_label.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=0)
        
        self.chosen_img_path_label = ctk.CTkEntry(self, border_width=0, corner_radius=0, fg_color="#333333", placeholder_text="")
        self.chosen_img_path_label.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=0)
        
        self.choose_img_btn = ctk.CTkButton(self, text="Choose an Image", command=self.onChooseImageBtnClicked)
        self.choose_img_btn.grid(row=4, column=0, columnspan=1, sticky="ew", padx=10, pady=0)
        
        self.choose_img_btn_indicator = ctk.CTkEntry(self, width=0, border_width=0, corner_radius=6)
        self.choose_img_btn_indicator.grid(row=4, column=1, sticky="ew", padx=10, pady=10)
        
        self.chosen_img_mask_path_label = ctk.CTkEntry(self, border_width=0, corner_radius=0, fg_color="#333333", placeholder_text="")
        self.chosen_img_mask_path_label.grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=0)
        
        self.choose_img_mask_btn = ctk.CTkButton(self, text="Choose a Mask", command=self.onChooseImageMaskBtnClicked)
        self.choose_img_mask_btn.grid(row=6, column=0, columnspan=1, sticky="ew", padx=10, pady=0)
        
        self.choose_mask_btn_indicator = ctk.CTkEntry(self, width=0, border_width=0, corner_radius=6)
        self.choose_mask_btn_indicator.grid(row=6, column=1, sticky="ew", padx=10, pady=10)
        
    def isValidImagePath(self, path):
        valid_image_formats = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff"]
        # Convert the path string to lowercase to handle case-insensitivity
        lowercase_path = path.lower()
        
        for format in valid_image_formats:
            if lowercase_path.endswith(format):
                return True
        return False
    
    def showImage(self):
        url = self._config.getOption("image_requests", "returned_url")
        response = requests.get(url)

        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            image_window = tk.Toplevel()
            image_window.title("Image from Web")

            photo = ImageTk.PhotoImage(image)

            image_label = tk.Label(image_window, image=photo)
            image_label.pack()
            image_label.mainloop()

        else:
            print("Failed to fetch the image from the web.")
            image_label.grid(row=0, column=0, sticky="nsew")
    
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
        
        if self.isValidImagePath(_path):
            self.show_img_btn.configure(state="normal")
            self.chosen_img_path_label.configure(placeholder_text=f"{_path}")
            self.choose_img_btn_indicator.configure(fg_color="#2a9d8f", text_color="#000000", placeholder_text="Good")
            self._config.openConfig()
            self._config.setOption("image_requests", "img_path", _path)
            self._config.saveConfig()
        else:
            self.show_img_btn.configure(state="disabled")
            self.chosen_img_path_label.configure(placeholder_text="Unsupported image file type!")
            self.choose_img_btn_indicator.configure(fg_color="#ff595e", text_color="#000000", placeholder_text="Bad")
        
    def onChooseImageMaskBtnClicked(self) -> False:
        _path = self.openFileDialog()
        if _path == False:
            return False
        
        if self.isValidImagePath(_path):
            self.chosen_img_mask_path_label.configure(placeholder_text=f"{_path}")
            self.choose_mask_btn_indicator.configure(fg_color="#2a9d8f", text_color="#000000", placeholder_text="Good")
            self._config.openConfig()
            self._config.setOption("image_requests", "mask_path", _path)
            self._config.saveConfig()
        else:
            self.choose_mask_btn_indicator.configure(fg_color="#ff595e", text_color="#000000", placeholder_text="Bad")
            self.chosen_img_mask_path_label.configure(placeholder_text="Unsupported image file type")
            
    def onImageSizeSelected(self, _size: str) -> None:
        self._config.openConfig()
        self._config.setOption("image_requests", "img_size", f"{_size}")
        self._config.saveConfig()
