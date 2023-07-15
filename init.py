from wingtpcli import WinGTPCLI
from bin import setup
import subprocess

class Initialize:
    def __init__(self, gui: bool) -> None:
        self._setup = setup.Setup()
        if gui:
            self.runWinGTPGUI()
        else:
            self.runWinGTPCLI()
        
    def runWinGTPGUI(self) -> None:
        subprocess.run(["python", "wingtpgui.py"])

    def runWinGTPCLI(self) -> None:
        API_KEY_PATH = './.api_key.conf'
        wingtp_cli = WinGTPCLI()
        wingtp_cli.setAPIKeyPath(API_KEY_PATH)
        wingtp_cli.converse()
    

def wingtp_gui_init(gui: bool) -> None:
    init = Initialize(gui)

wingtp_gui_init(True)
