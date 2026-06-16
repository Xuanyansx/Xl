def get_input():
    return list(map(int,input().split()))

def check(x):
    temp = 0
    last_i = 0
    for i in range(N):
        if a[i] - last_i < x:
            temp+=1
        else:
            last_i = a[i]
    if L - last_i < x:
        temp +=1
    return temp<=M

L,N,M = get_input()
a = [int(input()) for _ in range(N)]

l = 1
r = L

while l<=r:
    mid = (l+r)//2

    if check(mid):
        ans = mid
        l = mid+1
    else:
        r = mid-1

print(ans)