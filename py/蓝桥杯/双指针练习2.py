def get_input():
    return list(map(int,input().split()))

n,m,k = get_input()
a = get_input()

ans = 0

for l in range(n):
    count = 0
    for i in range(l,n):
        if a[i]>=m:
            count+=1

        if count==k:
            ans+=n-i
            break

print(ans)






"""
0 1
0 1 2 
0 1 2 3
0 1 2 3 4
0 1 2 3 4 5
0 1 2 3 4 5 6

1 2
1 2 3
1 2 3 4
1 2 3 4 5
1 2 3 4 5 6

2 3
2 3 4
2 3 4 5
2 3 4 5 6

3 4
3 4 5
3 4 5 6

4 5
4 5 6

5 6



"""