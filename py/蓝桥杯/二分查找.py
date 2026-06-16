def get_input():
    return list(map(int,input().split()))

n,k = get_input()
a = []

for i in range(n):
    a.append(get_input())

def check(x):
    cut = 0
    for h,w in a:
        cut += (h//x)*(w//x)
    return cut>=k

l = 1
r = 10**5
ans = 0

while l<=r:
    mid = (l+r)//2
    if check(mid):
        ans = mid
        l = mid+1
    else:
        r = mid-1
print(ans)