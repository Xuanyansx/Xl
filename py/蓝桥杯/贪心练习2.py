w = int(input())
n = int(input())

a = [int(input()) for _ in range(n)]
a.sort()
print(a)

ans = 0
while True:
    print(a)
    try:
        if a[0] + a[-1]<=w:
            ans+=1
            a.pop(0)
            a.pop(-1)
        else:
            ans+=1
            a.pop(-1)
    except:
        break

print(ans)