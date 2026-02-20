n,k = list(map(int,input().split()))
a = [int(input()) for _ in range(k)]
l = 1
r = 2*n

a.sort()
def check(x):
    d = x//2
    temp = 0
    for i in a:
        ll = temp+1
        if i-ll>d:
            return False
        if i-ll<0:
            ll = i
        rr = d+i-(i-ll)
        temp = rr
    return temp>=n
        


while l<=r:
    mid = (l+r)//2
    if check(mid):
        ans = mid
        r = mid-1
    else:
        l = mid+1
print(ans)



"""

2026/2/20 wq,a组的题目我都写出来了，虽然说研究了三天，太激动了，我要好好欣赏下我的代码

1 2 3 4 5 6 7 8 9 0
        +

x = 6


l = ri-n
r = ri+n

"""