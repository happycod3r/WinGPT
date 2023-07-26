

def printFuncName(func):
    print(func.__name__ + "()")
    
def myCoolFunction(a: int, b: int) -> int:
    return a + b

printFuncName(myCoolFunction)
