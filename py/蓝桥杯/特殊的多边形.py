from itertools import accumulate as acc
from collections import deque
from bisect import bisect_left,bisect_right


def get_input():
    return list(map(int,input().split()))

def check(a,b):
    """
    a:周长 
    b:最长边
    """
    return a-b>b

def dfs(x,a,b):
    """
    a:周长
    b:乘积
    """
    if x==n:
        if check(a,path[-1]):
            ans.append(b)
        return
    
    for i in range(1,max_r+1):
        if b*i>max_r:
            break

        if i<=path[-1]:
            continue
        
        path.append(i)
        a+=i
        b*=i
        dfs(x+1,a,b)
        path.pop(-1)
        a-=i
        b//=i    

t,n = get_input()
max_r = 0
cx = []
path = [0]


for _ in range(t):
    l,r = get_input()
    cx.append((l,r))
    max_r = max(max_r,r)


ans = []
dfs(0,0,1)
ans.sort()
for i,j in cx:
    l,r = bisect_left(ans,i),bisect_right(ans,j)
    res = r - l
    print(res)





    """
from itertools import accumulate as acc
from collections import deque
from bisect import bisect_left,bisect_right


def get_input():
    return list(map(int,input().split()))

def check(a,b):
    """
    a:周长 
    b:最长边
    """
    return a-b>b

def dfs(x,a,b):
    """
    a:周长
    b:乘积
    """
    if x==n:
        if check(a,path[-1]):
            ans.append(b)
        return
    
    for i in range(1,max_r+1):
        if b*i>max_r:
            break

        if i<=path[-1]:
            continue
        
        path.append(i)
        a+=i
        b*=i
        dfs(x+1,a,b)
        path.pop(-1)
        a-=i
        b//=i    

t,n = get_input()
max_r = 0
cx = []
path = [0]


for _ in range(t):
    l,r = get_input()
    cx.append((l,r))
    max_r = max(max_r,r)


ans = []
dfs(0,0,1)
ans.sort()

for i,j in cx:
    l,r = bisect_left(ans,i),bisect_right(ans,j)
    res = r - l
    print(res)





    """

    """


这个可以过90%，剩下一个超时


但是
from itertools import accumulate as acc
from collections import deque
from bisect import bisect_right,bisect_left


def get_input():
    return list(map(int,input().split()))

def check(a,b):
    """
    a:周长 
    b:最长边
    """
    return a-b>b

def dfs(x,a,b):
    """
    a:周长
    b:乘积
    """
    if x==n:
        if check(a,path[-1]):
            ans.append(b)
        return
    
    for i in range(1,max_r+1):
        if b*i>max_r:
            break

        if i<=path[-1]:
            continue
        
        path.append(i)
        a+=i
        b*=i
        dfs(x+1,a,b)
        path.pop(-1)
        a-=i
        b//=i    

t,n = get_input()
max_r = 0
cx = []
path = [0]


for _ in range(t):
    l,r = get_input()
    cx.append((l,r))
    max_r = max(max_r,r)


ans = []
dfs(0,0,1)
ans.sort()
for i,j in cx:
    res = bisect_right(ans,j) - bisect_left(ans,i)
    print(res)


"""
多边形需要满足任意其他边加起来大于另一条边

1 2 3
1 2 3 4
5 2 3 4
120

"""



这个却可以过100%

from itertools import accumulate as acc
from collections import deque
from bisect import bisect_left,bisect_right


def get_input():
    return list(map(int,input().split()))

def check(a,b):
    """
    a:周长 
    b:最长边
    """
    return a-b>b

def dfs(x,a,b):
    """
    a:周长
    b:乘积
    """
    if x==n:
        if check(a,path[-1]):
            ans.append(b)
        return
    
    for i in range(1,max_r+1):
        if b*i>max_r:
            break

        if i in path or i<=path[-1]:
            continue
        
        path.append(i)
        a+=i
        b*=i
        dfs(x+1,a,b)
        path.pop(-1)
        a-=i
        b//=i    

t,n = get_input()
max_r = 0
cx = []
path = [0]


for _ in range(t):
    l,r = get_input()
    cx.append((l,r))
    max_r = max(max_r,r)


ans = []
dfs(0,0,1)
ans.sort()
for i,j in cx:
    l,r = bisect_left(ans,i),bisect_right(ans,j)
    res = r - l
    print(res)





    """

    """

这个也是100%


wdf,这是什么原理，玄学吗，我这是真的不理解了

    """