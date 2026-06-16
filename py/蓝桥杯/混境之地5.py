from functools import lru_cache
from itertools import accumulate
from collections import deque
from bisect import bisect_left,bisect_right

def get_input():
    return list(map(int,input().split()))

def dfs(pos,is_k=True):
    """
    !!坐标格式(y,x)!!
    pos 当前坐标
    last_pos 上一个坐标
    k 再次之前是否使用过喷气背包
    """
    if pos == (c-1,d-1):
        global ans
        ans = "Yes"
        return
    
    for i,j in [(-1,0),(1,0),(0,1),(0,-1)]:
        if ans == "Yes":
            return
        y,x = pos[0]+i , pos[1]+j
        if y<0 or x<0 or (y,x) in path or y>n-1 or x>m-1:
            continue

        if Map[y][x]>Map[pos[0]][pos[1]]:
            if is_k:
                is_k = False
            else:
                continue
        path.append((y,x))
        
        dfs((y,x),is_k)
        path.pop(-1)
        if Map[y][x]>Map[pos[0]][pos[1]]:
            is_k = True



n,m,k = get_input()
a,b,c,d = get_input()
Map = []
path = [(a-1,b-1)]
ans = "No"

for i in range(n):
    Map.append(get_input())

dfs((a-1,b-1))
print(ans)


"""

20 6 74
5 5 6 6
52 37 86 54 89 55
5 13 51 86 84 68
85 1 97 18 63 46
4 19 39 13 59 39
33 7 86 72 11 89
2 43 11 28 36 12


"""