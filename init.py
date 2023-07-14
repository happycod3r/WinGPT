from bin import setup
import subprocess

class Initialize:
    def __init__(self) -> None:
        self._setup = setup.Setup()
        
    def runWinGTPGUI(self) -> None:
        subprocess.run(["python", "wingtpgui.py"])

def wingtp_gui_init() -> None:
    init = Initialize()
    init.runWinGTPGUI()

wingtp_gui_init()
