from itertools import accumulate
from collections import deque

n = int(input())
a = [int(i) for i in input().split()]
vis = [1]*n
ans = 0


for i in range(n):
    if vis[i] ==0:
        continue
    vis[i] = 0
    for j in range(n):
        if vis[j] ==0 or a[i]%a[j]==0 or a[j]%a[i]==0:
            continue
        vis[j] = 0

    ans+=1

print(ans)







    
    


            
