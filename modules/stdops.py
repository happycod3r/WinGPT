import os

class StdOps:
    def __init__(self) -> None:
        pass
    
    def createDir(self, path: str) -> bool:
        if not os.path.exists(path):
            try:
                os.mkdir(path)
                return True
            except FileNotFoundError:
                print("FileNotFoundError: File not found error")
                return False
            except IOError:
                print("IOError: Could not create directory.")
            except Exception as e:
                print(repr(e))
                return False
        return True        
    
    def createFile(self, file_path: str) -> bool:
        if not os.path.exists(file_path):
            try:
                with open(file_path, 'w') as file:
                    file.close()
                    return True
            except FileNotFoundError:
                print(f"File '{file_path}' already exists!")
                return False
            except IOError:
                return False
            except Exception as e:
                print(repr(e))
                return False
                    
    def writeTofile(self, file_path: str, content: str = None, _mode: str = "w") -> bool:
        if os.path.exists(file_path):
            try:
                with open(f"{file_path}", f"{_mode}") as file:
                    if len(content) != 0:
                        if file.writable():
                            file.write(content)
                            file.close()
                            return True
                        else: 
                            return False
                    return False
            except FileNotFoundError:
                print(f"File '{file_path}' not found!")
                return False
            except IOError:
                print(f"An error occurred while creating the file '{file_path}'.")
                return False
            except Exception as e:
                print(f"An error occurred while creating the file '{file_path}'.")
                return False
        return False
    
    def readFromFile(self, file_path: str) -> (str | bool):
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as file:
                    contents = file.read()
                    if len(contents) != 0:
                        return contents
                    else: 
                        print(f"File @'{file_path}' is exists but is empty")
                        return False
            except FileNotFoundError:
                print(f"File '{file_path}' not found.")
                return False
            except IOError:
                print(f"Error reading file '{file_path}'.")
                return False
            except Exception as e:
                print(repr(e))
                return False
        return False
        