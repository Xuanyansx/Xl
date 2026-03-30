from itertools import accumulate
from collections import deque
from bisect import bisect_left,bisect_right
def fun(n):
    if n==1 or n==0:
        return 1
    
    temp = jl.get(n,0)
    
    if temp == 0:
        jl[n] = fun(n-1)+fun(n-2)
        return jl[n]
    return temp

jl = {}


print(fun(40))

"""




"""