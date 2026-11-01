# class a:
#     def __init__(self):
#         pass
#     def __post_init__(self):
#         print(self.v)


# aa = a()
# aa.v = 1
# print(aa.v)


import prompt_toolkit

def a():
    while True:
        u = prompt_toolkit.prompt("[ ]< ")
        a = yield u
        print(f"<><>{a}")


def b():
    func = a()
    u = next(func)

    while True:
        us = yield u
        u = func.send(us)
        
func = b()
us = next(func)

while True:
    us = func.send(f"{us}+{us}")
    

    

