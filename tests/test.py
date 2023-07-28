
# def genAI():
#     a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#     for i in range(len(a)):
#         b = input("enter a number: ")
#         if int(b) == a[i]:
#             yield b

# index = 0
# c = []

# for value in genAI():
#     c.append(value)
#     index = index + 1
# print(repr(c))
    
    
def echo_type():
    prompt = ":>> "
    while True:
        inpt = input(F"{prompt}")
        yield inpt

def output(inpt: str):
    print(inpt)

for value in echo_type():
    output(value)
