def get_input():
    return list(map(int,input().split()))


def get_sum(L,n):
    for i in range(1,n):
        L[i] = L[i]+L[i-1]
    return L

def get_ans(l,r,L):
    l = l-1
    r = r-1
    if l == 0:
        return L[r]
    return L[r]-L[l-1]


n,m = get_input()
a = get_input()

a_sum = [0]*6
for i in range(1,6):
    L = [x**i for x in a]
    a_sum[i] = get_sum(L,n) 


for i in range(m):
    l,r,k = get_input()
    ans = get_ans(l,r,a_sum[k]) % (10**9+7)
    print(ans)