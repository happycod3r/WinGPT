from win_gtp import WinGTP
import subprocess

USE_GUI = True

if USE_GUI == True:
    subprocess.run(["python", "gui.py"])
else:
    API_KEY_PATH = './.api_key.conf'
    newRequest = WinGTP()
    newRequest.setAPIKeyPath(API_KEY_PATH)
    newRequest.converse()
