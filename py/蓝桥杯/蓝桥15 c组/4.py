



"""

[
    [0,1],[0,2],[9,0],[8,1],[4,2]
]



"""
from itertools import accumulate

def check(a,left,right):
    left_v,left_d = a[left]
    right_v,right_d = a[right]

    if left_v == right_v:
        return left_d > right_d
    return left_v > right_v

def px(a,left=None,right=None):
    if left==right==None:
        left = 0
        right = len(a)-1
    l = left
    r = right
    point = left

    if not(left<right):
        return
    
    while left<right:
        if check(a,left,right):
            a[left],a[right] = a[right],a[left]
            if point == left:
                point = right
            else:
                point = left
        
        if point == left:
            right-=1
        else:
            left+=1
    
    px(a,l,right-1)
    px(a,left+1,r)

bh = {
    '0':1,
    '4':1,
    '6':1,
    '8':2,
    '9':1
}

v = []
n = int(input())
for i in input().split():
    quan = 0
    for j in i:
        quan+= bh.get(j,0)
    v.append([quan,int(i)])

px(v)
temp = ""
for i in v:
    temp+=f"{i[1]} "
print(temp)