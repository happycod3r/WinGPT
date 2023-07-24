import setup
import gui
import os
import logger


"""
# TODO FIRST THING!
- Finish key config parser
- clean up cli the best I can.  
"""

class Initialize:
    def __init__(self) -> None:
        self.CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
        self.CONFIG_DIR = f"{self.CURRENT_PATH}\\config"
        self.GUI_SHOWN_FLAG_FILE = f"{self.CONFIG_DIR}\\.gui.flag"
        self.SETUP_DONE_FLAG_FILE = f"{self.CONFIG_DIR}\\.setup.flag"
        self.log = logger.LogManager()
        if os.path.exists(self.SETUP_DONE_FLAG_FILE):
            self.runWinGTPGUI()
        else:
            self.runWinGTPSetup()
            # If the gui was never shown and setup was canceled
            # if not os.path.exists(self.GUI_SHOWN_FLAG_FILE):
            #     self.cleanUpAfterSelf()
            
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
