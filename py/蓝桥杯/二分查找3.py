def check(x):
    temp = 0
    for i in range(1,n+1):
        temp+=min(m,(x//i))
    return temp<k

n,m,k = list(map(int,input().split()))


l = 1
r = m*n

while l<=r:
    mid = (l+r)//2
    if check(mid):
        l=mid+1
    else:
        ans = mid
        r=mid-1


print(ans)