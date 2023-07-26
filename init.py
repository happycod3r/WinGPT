import setup
import gui
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev & PyInstaller. """
    try:
        # PyInstaller creaes a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

Logo = resource_path("Logo.png")

class Initialize:
    def __init__(self) -> None:
        self.CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
        self.CONFIG_DIR = f"{self.CURRENT_PATH}\\config"
        self.GUI_SHOWN_FLAG_FILE = f"{self.CONFIG_DIR}\\.gui.flag"
        self.SETUP_DONE_FLAG_FILE = f"{self.CONFIG_DIR}\\.setup.flag"
        if os.path.exists(self.SETUP_DONE_FLAG_FILE):
            self.runWinGTPGUI()
        else:
            self.runWinGTPSetup()
            # If the gui was never shown and setup was canceled
            # if not os.path.exists(self.GUI_SHOWN_FLAG_FILE):
            #     self.cleanUpAfterSelf()
            
            # TOFIX: I'm getting the following warning when the setup window is closed.
            # I don't think the setup window is being destroyed properly. I don't want
            # it to cause memory leaks or any other unwanted side effects. So far
            # so good though. Nothing to report.
            # 
            # invalid command name "1705901111680update"
            # while executing "1705901111680update" ("after" script)
            # invalid command name "1705899062592check_dpi_scaling" 
            # while executing "1705899062592check_dpi_scaling" ("after" script)
            
    def cleanUpAfterSelf(self) -> None:
        print("Setup failed. Rolling back changes")
        try:
            if os.path.exists(self.SETUP_DONE_FLAG_FILE):
                os.remove(self.SETUP_DONE_FLAG_FILE)
                
            if os.path.exists(self.USER_SETTINGS_FILE):
                os.remove(self.USER_SETTINGS_FILE)
            
            if os.path.exists(self.KEY_CONFIG_FILE):
                os.remove(self.KEY_CONFIG_FILE)
            
            if os.path.exists(self.CONFIG_DIR):
                os.rmdir(self.CONFIG_DIR)
            
            if os.path.exists(self.LOGS_DIR):
                os.rmdir(self.LOGS_DIR) 
        except IOError as ioe:
            print(repr(ioe))
        except Exception as e:
            print(repr(e))  
    
    def runWinGTPGUI(self) -> None:
        self.gui = gui.WinGTPGUI()
        self.gui.mainloop()
        
    def runWinGTPSetup(self) -> None:
        self.setup = setup.Setup()
        self.setup.mainloop()
    
def wingtp_gui_init() -> None:
    init = Initialize()     

wingtp_gui_init()
