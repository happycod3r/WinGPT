import subprocess

def execSH(script_path):
    subprocess.run(['bash', script_path], shell=True)
    return True

def execPS1(script_path):
    subprocess.run(['powershell', '-File', script_path], shell=True)

def sayhi():
    print("hello")
