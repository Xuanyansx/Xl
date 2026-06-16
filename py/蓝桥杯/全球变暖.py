import os
import sys

from itertools import accumulate
from collections import deque
sys.setrecursionlimit(20000)



def dfs(y,x):
    global vis
    global flag

    vis[y][x] = 0
    temp = True
    for i in fx:
        xx,yy = x+i[0],y+i[1]
        if Map[yy][xx] == '.':
            temp = False       

        if vis[yy][xx] and Map[yy][xx] == "#":
            dfs(yy,xx)
        
    if temp:
        flag = False

n = int(input())
Map = []
ans = 0
fx = [(-1,0),(1,0),(0,-1),(0,1)]
vis = [[1]*n for _ in range(n)]

for i in range(n):
    Map.append(list(input()))


for x in range(n):
    for y in range(n):
        if Map[y][x] == '#' and vis[y][x]:
            flag = True
            dfs(y,x)
            if flag:
                ans+=1

print(ans)



        


    