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
        self.TMP_DIR = f"{self.CURRENT_PATH}\\..\\tmp"
        self.IMG_URL = self.getImageURL()
        
        self.img = ctk.CTkImage(light_image=None, dark_image=self.loadImageFromUrl(), size=(400, 400))
        self._label = ctk.CTkLabel(self, image=self.img, text=" ")
        self._label.grid(row=0, column=0)
        self._label.configure(width=400, height=400)
        
    def loadImageFromUrl(self):
        _response = requests.get(self.IMG_URL)
        _image_data = _response.content
        return Image.open(BytesIO(_image_data))

    def getImageURL(self):
        _url = self.stdops.readFromFile(f"{self.TMP_DIR}\\img_url.tmp")
        if _url is not False:
            return _url
        return False

# def showImageView():
#     _stdops = stdops.StdOps()
    
#     CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
#     TMP_DIR = f"{CURRENT_PATH}\\..\\tmp"
    
#     _url = _stdops.readFromFile(f"{TMP_DIR}\\img_url.tmp")
    
#     _response = requests.get(_url)
#     _image_data = _response.content
    
#     img_view = ctk.CTkToplevel()
#     img_view.geometry("500x500")
    
#     _img = ctk.CTkImage(light_image=None, dark_image=Image.open(BytesIO(_image_data)), size=(400, 400))
    
#     _label = ctk.CTkLabel(img_view, image=_img, text=" ")
#     _label.grid(row=0, column=0)
#     _label.configure(width=500, height=500)
    
