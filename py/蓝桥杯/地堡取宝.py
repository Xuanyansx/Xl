from itertools import accumulate
from collections import deque
from bisect import bisect_left,bisect_right
from functools import lru_cache


def get_input():
    return list(map(int,input().split()))

n,m,k = get_input()
Map = []
ans = 0

def dfs(x,y,o,w):

    if x==m-1 and y==n-1:
        if  o==k :
            global ans
            ans+=1
            print(path)
        return
    

    for i,j in [(0,1),(1,0)]:
        xx,yy = x+i,y+j
        if xx>=m or yy>=n:
            continue
        temp_w = Map[yy][xx]

        path.append(temp_w)

        if temp_w>w:
            if o<k:
                dfs(xx,yy,o+1,temp_w)
            dfs(xx,yy,o,w)
        else:
            dfs(xx,yy,o,w)
        path.pop(-1) 
        
         


for i in range(n):
    Map.append(get_input())


path = []
dfs(0,0,0,-1)
dfs(0,0,1,Map[0][0])

print(ans)