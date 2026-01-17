

n = input()
k = int(input())

nums = '123456789abcdef'

ans = 0
for i in :
    ans+=int(n[::-1][i])*k**i
print(ans)