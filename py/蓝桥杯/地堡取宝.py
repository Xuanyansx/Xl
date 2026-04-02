from itertools import accumulate
from collections import deque
from bisect import bisect_left,bisect_right
from functools import lru_cache


def get_input():
    return list(map(int,input().split()))

n,m,k = get_input()
Map = []
ans = 0



@lru_cache(None)
def dfs(x,y,o,w):
    temp_w = Map[y][x]
    ans = 0
    if x==m-1 and y==n-1:
        if o == k:
            return 1
        if temp_w>w and o==k-1:
            return 1
        return 0    
            


    for i,j in [(0,1),(1,0)]:
        xx,yy = x+i,y+j
        if xx>=m or yy>=n:
            continue

        if temp_w > w:
            if o<k:
                ans += dfs(xx,yy,o+1,temp_w)
        ans+=dfs(xx,yy,o,w)
    t = (10**9)+7 
    return ans%t

for i in range(n):
    Map.append(get_input())

ans = dfs(0,0,0,-1)
print(ans)
