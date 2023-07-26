import customtkinter as ctk
from PIL import Image
from io import BytesIO
import requests
import os
import modules.stdops as stdops

class ImageView(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x400")
        self.stdops = stdops.StdOps()
        
        self.CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
        self.TMP_DIR = f"{self.CURRENT_PATH}\\..\\tmp"
        self.IMG_URL = self.getImageURL()
        
        self.img = ctk.CTkImage(dark_image=self.loadImageFromUrl(), size=(400, 400))
        self.label = ctk.CTkLabel(self, text="", image=self.img)
        self.label.grid(row=0, column=0)
        self.label.configure(width=400, height=400)

    def loadImageFromUrl(self):
        _response = requests.get(self.IMG_URL)
        _image_data = _response.content
        return Image.open(BytesIO(_image_data))

    def getImageURL(self):
        _url = self.stdops.readFromFile(f"{self.TMP_DIR}\\img_url.tmp")
        if _url is not False:
            self.IMG_URL = _url
            return _url
        return False
