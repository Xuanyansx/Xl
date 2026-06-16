import os
import sys
sys.setrecursionlimit(10000)
def dfs(x):
    path.append(x)
    if a[x] in path:
        if a[x] == i:
            global ans
            global ans_path
            ans = max(ans,len(path))
            ans_path+= path
        return
    dfs(a[x])

n = int(input())
a = [0]+[int(i) for i in input().split()]

ans = 0
ans_path = []

for i in range(1,n+1):
    path = []
    if a[i] in ans_path:
        continue
    dfs(i)

print(ans)