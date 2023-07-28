import paths
import customtkinter as ctk
from PIL import Image
from io import BytesIO
import requests
import os
import modules.stdops as stdops

class ImageView(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("400x400")
        self.stdops = stdops.StdOps()
        
        self.CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
        self.TMP_DIR = paths.TMP_DIR
        self.IMG_URL = self.getImageURL()
        
        self.img = ctk.CTkImage(light_image=None, dark_image=self.loadImageFromUrl(), size=(400, 400))
        self._label = ctk.CTkLabel(self, image=self.img, text=None)
        self._label.grid(row=0, column=0)
        self._label.configure(width=400, height=400)
        
    def loadImageFromUrl(self):
        _response = requests.get(self.IMG_URL)
        _image_data = _response.content
        return Image.open(BytesIO(_image_data))

    def getImageURL(self):
        _url = self.stdops.readFromFile(f"{paths.TMP_IMAGE_URL_FILE}")
        if _url is not False:
            return _url
        return False
