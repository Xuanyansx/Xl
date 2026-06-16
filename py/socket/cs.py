# import socket as sk

# s = sk.socket()

# a = sk.gethostname()
# print(a)


# a = ["1","2","s"]

import asyncio
async def a():
    print("1")
    await asyncio.sleep(1)
    print('11')

async def b():
    print("2")
    await asyncio.sleep(1)
    print('22')

task = [a(),b()]
asyncio.run(asyncio.wait(task))