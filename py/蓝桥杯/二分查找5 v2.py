

"""

前缀和重制版

"""
n = int(input())
a = list(map(int,input().split()))

max_a = max(a)+1


ac = [0]*max_a
prefix = []

temp=0
l = 0
r = max_a-1


index = 0

for i in a:
    ac[i]+=1

for i in ac:
    prefix.append(temp+i)
    temp+=i

def check(x,t=0):
    if x == 0:
        less = 0
    else:
        less = prefix[x-1]

    greater = prefix[max_a-1] - prefix[x]
    if t:
        return less,greater
    return less>=greater


while l<=r:
    mid = (r+l)//2
    if check(mid):
        index = mid
        r = mid-1
    else:
        l = mid+1


l,g = check(index,t=1)
if l<=g:
    index+=1
    

for i in a:
    if (l==g and i==index-1) or index<i:
        res = 0
    else:
        res = index-i
    print(f"{res}",end=" ")











