import customtkinter as ctk
from PIL import ImageTk, Image
from io import BytesIO
import requests
import os

class ImageView(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x400")
        
        self.CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
        self.IMG_URL = self.getImageURL()
        
        self.img = ctk.CTkImage(dark_image=self.loadImageFromUrl(), size=(400, 400))
        self.label = ctk.CTkLabel(self, text="", image=self.img)
        self.label.grid(row=0, column=0)
        self.label.configure(width=400, height=400)
        self.focus()

    def loadImageFromUrl(self):
        _response = requests.get(self.IMG_URL)
        _image_data = _response.content
        return Image.open(BytesIO(_image_data))

    def getImageURL(self):
        try:
            with open(f"{self.CURRENT_PATH}\\..\\config\\img_url.tmp") as file:
                _url = file.read()
                file.close()
                return _url
        except FileNotFoundError:
            return False
        except IOError:
            return False
        except Exception as e:
            print(repr(e))
            return False
