n = int(input())
a = list(map(int,input().split()))



ans = 0
while True:
    a2 = [0]*n  
    a2[0] = int(a[n-1]/2)
    for j in range(n-1):
        
        a2[j+1] = int(a[j]/2)
        a2[j] += int(a[j]/2)
    a2[n-1] += int(a[n-1]/2)
    a = a2
    for i in range(n):
        if a[i]%2==1:
            a[i]+=1
            ans+=1

    if len(set(a)) == 1:
        break
print(ans)


# 2 2 4
# 1 1 2
# 2 1 1

# 3 2 3
"""
2 2 4

3 2 3

4 2 4

4 4 3


"""