n = int(input())
a = []
temp = 0
c_a = {}
max_a = 0
ans = 0

for i in (input().split()):
    i = int(i)
    if i>max_a:
        max_a = i
    temp ^= i
    a.append(temp)
    c_a[temp] = c_a.get(temp,0)+1


print(a)
ss = []
for i in range(max_a):
    temp = i*i
    for j in range(n):
        res = a[j]^temp
        if res in a and res<=a[j]:
            ans+=1
print((n*(n+1)//2)-ans)
# print(a)
# for i in range(n):
#     for j in range(i,n):
#         print(f"{a[i] if i==0 else a[i-1]}-{a[j]}={yh(i,j)}",end=" ")
#     print()


"""

1-1=1 1-3=3 1-0=0 1-4=4 1-1=1
1-3=2 1-0=1 1-4=5 1-1=0
3-0=3 3-4=7 3-1=2
0-4=4 0-1=1
4-1=5

1-1 3-3 0-0 4-4 1-1

0-1 2-3 1-0 5-4 0-1
5-1 7-3 4-0 0-4 5-1

8-1 10-3 9-0 13-4 8-1
17-1 19-3 16-0 20-4 17-1

"""