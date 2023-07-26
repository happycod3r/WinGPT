
class Debug:
    
    def __init__(self):
        
        self.DEBUG = True

    def out(self, data: str) -> None:
        print(f"{data}()")
        
    def track(self, func_name: str) -> None:
        print(f"{func_name.__name__}()")
