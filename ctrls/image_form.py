import customtkinter as ctk
from tkinter import filedialog
import os
import modules.persistence as persistence
from ctrls import image_view
import cli

class ImageForm(ctk.CTkScrollableFrame):
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
        self.cli = cli.OpenAIInterface()
    
        self.title = ctk.CTkLabel(self, text="Images")
        self.title.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=0)
        
        self.size_menu = ctk.CTkOptionMenu(
            self, 
            dynamic_resizing=False, 
            values=["256x256", "512x512", "1024x1024"],
            command=self.onImageSizeSelected
        )
        self.size_menu.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        #////////////
        
        self.chosen_img_path_label = ctk.CTkEntry(self, border_width=0, corner_radius=6, fg_color="#333333", placeholder_text="")
        self.chosen_img_path_label.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=0)
        #////////////
        
        self.choose_img_btn = ctk.CTkButton(self, text="Choose an Image", command=self.onChooseImageBtnClicked)
        self.choose_img_btn.grid(row=3, column=0, columnspan=1, sticky="ew", padx=10, pady=0)
        
        self.choose_img_btn_indicator = ctk.CTkLabel(self, width=0, corner_radius=6, fg_color="#333333", text="")
        self.choose_img_btn_indicator.grid(row=3, column=1, sticky="ew", padx=10, pady=10)
        #////////////
        
        self.chosen_img_mask_path_label = ctk.CTkEntry(self, border_width=0, corner_radius=6, fg_color="#333333", placeholder_text="")
        self.chosen_img_mask_path_label.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=0)
        #////////////
        
        self.choose_img_mask_btn = ctk.CTkButton(self, text="Choose a Mask", command=self.onChooseImageMaskBtnClicked)
        self.choose_img_mask_btn.grid(row=5, column=0, columnspan=1, sticky="ew", padx=10, pady=0)
        
        self.choose_mask_btn_indicator = ctk.CTkLabel(self, width=40, corner_radius=6, fg_color="#333333", text="")
        self.choose_mask_btn_indicator.grid(row=5, column=1, sticky="ew", padx=10, pady=10)
        #////////////
        
        self.use_edit_switch = ctk.CTkSwitch(self, text="Make image edit", command=self.onUseEditSwitchChanged)
        self.use_edit_switch.grid(row=6, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        self.use_edit_switch.grid_rowconfigure(0, weight=1)
        
        self.use_variation_switch = ctk.CTkSwitch(self, text="Make image variation", command=self.onUseVariationSwitchChanged)
        self.use_variation_switch.grid(row=7, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        self.use_variation_switch.grid_rowconfigure(0, weight=1)
        
        self.use_new_switch = ctk.CTkSwitch(self, text="Make new image", command=self.onUseNewSwitchChanged)
        self.use_new_switch.grid(row=8, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        self.use_new_switch.grid_rowconfigure(0, weight=1)
        
        self.show_img_btn = ctk.CTkButton(
            self, 
            text="Show",  
            command=self.showImage, 
            width=60)
        
        
        self.show_img_btn.grid(row=9, column=0, sticky="nsew", padx=10, pady=10)
        #////////////
        self.loadOptions()
            
    def loadOptions(self):
        if self.cli.getUseImageEdit() == 1:
            self.use_edit_switch.select()
            self.onUseEditSwitchChanged()
        elif self.cli.getUseImageVariation() == 1:
            self.use_variation_switch.select()
            self.onUseVariationSwitchChanged()
        elif self.cli.getUseImageNew() == 1:
            self.use_new_switch.select()
            self.onUseNewSwitchChanged()
    
    def onUseEditSwitchChanged(self):
        _use_edit = self.use_edit_switch.get()
        if _use_edit == 1:
            self.cli.setUseImageEdit(1)
            self.use_variation_switch.configure(state="disabled")
            self.use_new_switch.configure(state="disabled")
        else:
            self.cli.setUseImageEdit(0)
            self.use_variation_switch.configure(state="normal")
            self.use_new_switch.configure(state="normal")
                
    def onUseVariationSwitchChanged(self):
        _use_variation = self.use_variation_switch.get()
        if _use_variation == 1:
            self.cli.setUseImageVariation(1)
            self.use_edit_switch.configure(state="disabled")
            self.use_new_switch.configure(state="disabled")
            # Disable anything not needed for a variation.
            self.choose_img_mask_btn.configure(state="disabled")
            self.chosen_img_mask_path_label.configure(state="disabled")
        else:
            self.cli.setUseImageVariation(0)
            self.use_edit_switch.configure(state="normal")
            self.use_new_switch.configure(state="normal")
            self.choose_img_mask_btn.configure(state="normal")
            self.chosen_img_mask_path_label.configure(state="normal")
            
    def onUseNewSwitchChanged(self): 
        _use_new = self.use_new_switch.get()
        if _use_new == 1: 
            self.cli.setUseImageNew(1)
            self.use_edit_switch.configure(state="disabled")
            self.use_variation_switch.configure(state="disabled")
            self.choose_img_mask_btn.configure(state="disabled")
            self.chosen_img_mask_path_label.configure(state="disabled")
            self.choose_img_btn.configure(state="disabled")
            self.chosen_img_path_label.configure(state="disabled")
        else:
            self.cli.setUseImageNew(0)
            self.use_edit_switch.configure(state="normal")
            self.use_variation_switch.configure(state="normal")
            self.choose_img_mask_btn.configure(state="normal")
            self.chosen_img_mask_path_label.configure(state="normal")
            self.choose_img_btn.configure(state="normal")
            self.chosen_img_path_label.configure(state="normal")
               
    def isValidImagePath(self, _path: str) -> bool:
        """
        Summary:
            Checks if the passed in string is a valid image path by 
            checking for a valid extension at the end of the string such
            as '.png' or '.jpg' and returns True if it is a valid path.
        Args:
            _path (str): The path to a valid image.

        Returns:
            (bool): True if valid otherwise False
        """
        valid_image_formats = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff"]
        if not os.path.exists(_path):
            return False
        # Convert to lowercase to handle case-insensitivity
        lowercase_path = _path.lower()
        for format in valid_image_formats:
            if lowercase_path.endswith(format):
                return True
        return False
    
    def showImage(self):
        img_view = image_view.ImageView()
        
    
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

