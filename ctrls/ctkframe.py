
import tkinter as tk
from typing import Any
import customtkinter as ctk

class CustomTkFrame(ctk.CTkFrame):
    def __init__(self, *args: Any, **kwds: Any) -> Any:
        super().__init__(*args, **kwds)
        self.configure(
            bg_color="transparent",
            fg_color="transparent",
            border_width=0,
            corner_radius=0,
        )
