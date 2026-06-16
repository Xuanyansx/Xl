import os
import sys

# 请在此输入您的代码


n = int(input())
a = input().split()

ans = 0
count_a = [0]*n

vis = [0]*n

for i in range(n):
    count_a[i] = a[i].count('6')

count_a.sort()
for i in range(n-1,-1,-1):
    path = []
    xl = 1
    temp = count_a[i]
    for j in range(i):
        if vis[j]:
            continue
        
        if temp>=6:
            break
        if xl==3:
            temp -= count_a[path.pop(0)]
            xl-=1
        path.append(j)
        temp+=count_a[j]
        xl+=1
    if temp<6:
        break
    ans+=1
    for j in path:
        vis[j] = 1
    

print(ans)





    


         
    




"""

7
666666 16166 6696 666 6 6 6

666666 16166666 6696 6 6

[1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 5, 5, 5, ]

"""
