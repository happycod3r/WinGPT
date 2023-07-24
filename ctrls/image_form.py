import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import os
import modules.persistence as persistence
from ctrls import image_view


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
        
        self.CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
        self._config = persistence.Persistence()
        
        self.img_view = None
        self.title = ctk.CTkLabel(self, text="Images")
        self.title.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=0)
        
        self.size_menu = ctk.CTkOptionMenu(
            self, 
            dynamic_resizing=False, 
            values=["256x256", "512x512", "1024x1024"],
            command=self.onImageSizeSelected
        )
        self.size_menu.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        
        self.show_img_btn = ctk.CTkButton(
            self, 
            text="Show",  
            command=self.showImage, 
            width=60)
        self.show_img_btn.grid(row=1, column=1, sticky="ew", padx=10, pady=10)
        
        self.path_label = ctk.CTkLabel(self, text="Path:")
        self.path_label.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=0)
        
        self.chosen_img_path_label = ctk.CTkEntry(self, border_width=0, corner_radius=6, fg_color="#333333", placeholder_text="")
        self.chosen_img_path_label.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=0)
        
        self.choose_img_btn = ctk.CTkButton(self, text="Choose an Image", command=self.onChooseImageBtnClicked)
        self.choose_img_btn.grid(row=4, column=0, columnspan=1, sticky="ew", padx=10, pady=0)
        
        self.choose_img_btn_indicator = ctk.CTkLabel(self, width=0, corner_radius=6, fg_color="#333333", text="")
        self.choose_img_btn_indicator.grid(row=4, column=1, sticky="ew", padx=10, pady=10)
        
        self.chosen_img_mask_path_label = ctk.CTkEntry(self, border_width=0, corner_radius=6, fg_color="#333333", placeholder_text="")
        self.chosen_img_mask_path_label.grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=0)
        
        self.choose_img_mask_btn = ctk.CTkButton(self, text="Choose a Mask", command=self.onChooseImageMaskBtnClicked)
        self.choose_img_mask_btn.grid(row=6, column=0, columnspan=1, sticky="ew", padx=10, pady=0)
        
        self.choose_mask_btn_indicator = ctk.CTkLabel(self, width=0, corner_radius=6, fg_color="#333333", text="")
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
        if self.img_view is None or not self.img_view.winfo_exists():
            self.img_view = image_view.ImageView(self, takefocus=True)
            
        else:
            self.img_view.focus()
        # try:
        #     with open(f"{self.CURRENT_PATH}\\..\\config\\img_url.tmp") as file:
        #         _url = file.read()
        #         file.close()
        #         self.IMG_URL = _url
        # except FileNotFoundError:
        #     return False
        # except IOError:
        #     return False
        # except Exception as e:
        #     print(repr(e))
        #     return False

        # root = tk.Toplevel()
        # img_url = f"{self.IMG_URL}"
        # response = requests.get(img_url)
        # img_data = response.content
        # img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
        # panel = tk.Label(root, image=img)
        # panel.pack(side="bottom", fill="both", expand="yes")
        # root.mainloop()
        
    
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
            self.choose_img_btn_indicator.configure(fg_color="#2a9d8f", corner_radius=6, text_color="#000000", text="Good")
            self._config.openConfig()
            self._config.setOption("image_requests", "img_path", _path)
            self._config.saveConfig()
        else:
            self.show_img_btn.configure(state="disabled")
            self.chosen_img_path_label.configure(placeholder_text="Unsupported image file type!")
            self.choose_img_btn_indicator.configure(fg_color="#ff595e", text_color="#000000", text="Bad")
        
    def onChooseImageMaskBtnClicked(self) -> False:
        _path = self.openFileDialog()
        if _path == False:
            return False
        
        if self.isValidImagePath(_path):
            self.chosen_img_mask_path_label.configure(placeholder_text=f"{_path}")
            self.choose_mask_btn_indicator.configure(fg_color="#2a9d8f", corner_radius=6, text_color="#000000", text="Good")
            self._config.openConfig()
            self._config.setOption("image_requests", "mask_path", _path)
            self._config.saveConfig()
        else:
            self.choose_mask_btn_indicator.configure(fg_color="#ff595e", text_color="#000000", text="Bad")
            self.chosen_img_mask_path_label.configure(placeholder_text="Unsupported image file type")
            
    def onImageSizeSelected(self, _size: str) -> None:
        self._config.openConfig()
        self._config.setOption("image_requests", "img_size", f"{_size}")
        self._config.saveConfig()
