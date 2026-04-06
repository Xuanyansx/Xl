from collections import deque
from itertools import accumulate
from functools import lru_cache

#n,m = list(map(int,input().split()))
n = 4
m = 7
dp = [1] * 1001
temp = []
for i in range(1,1001):
    res = 0
    a = 0
    b = 0
    if i-n>=0:
        a = dp[i-n]
    if i-m>=0:
        b = dp[i-m]
    dp[i] = res or a or b
    if dp[i] == 0:
        temp.append(i)
print(temp[-1])
