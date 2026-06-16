import os
import sys
 
# 请在此输入您的代码


def get_input():
    return list(map(int,input().split()))

n = get_input()
bl = get_input()

bl.sort()
ans = 0
while True:
    try:
        temp = bl[0]+bl[1]
    except :
        break
    bl.pop(0)
    bl[0] = temp
    ans += temp
    bl.sort()
print(ans)