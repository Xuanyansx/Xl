


def get_input():
    return list(map(int,input().split()))


n,S = get_input()
a = get_input()

l = 0
r = 0
sum_r = 0
ans = n+1

while l<=r and r<n:
    if sum_r>=S:
        temp = r-l
        if temp<ans:
            ans = temp
        sum_r-=a[l]
        l+=1
    else:
        sum_r+=a[r]
        r+=1
if ans == n+1:
    ans = 0
print(ans)
    
    