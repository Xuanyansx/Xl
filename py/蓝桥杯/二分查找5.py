

"""

这题目真拗口，看来几遍才看懂再说什么（（（（

"""
n = int(input())
a = list(map(int,input().split()))
ac = a.copy()
a.sort()


a_mid = a[n//2]
l = 0
r = n-1


while l<=r:
    mid = (l+r)//2
    if a[mid]>a_mid:
        r = mid-1
    else:
        right = mid
        l = mid+1

l = 0
r = n-1

while l<=r:
    mid = (l+r)//2
    if a[mid]>=a_mid:
        r = mid-1
        left = mid
    else:
        l = mid+1



if n-1-right < left:
    index = a[left]
else:
    index = a[right]+1

is_true = left == n-1-right


for i in ac:
    if (is_true and i==a[left])or i>index:
        res = 0
    else:
        res = index-i
    print(res,end=" ")



"""

0 0 1 1 1 1 1 2 2 2
        +   

5
12 10 15 20 6
6 10 12 15 20
7 3  0  0  0
10
2 2 1 1 1 1 1 0 0 0
0 0 0 1 1 1 1 1 2 2
2 2 2 0 0 0 0 0 0 0

10
0 0 1 1 1 1 1 2 2 2
2 2 1 1 1 1 1 0 0 0
"""




"""
12 10 15 20 6
12 22 37 57 63

1 2 6 10 12 15 20
"""

