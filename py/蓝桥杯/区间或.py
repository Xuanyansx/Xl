from itertools import accumulate

def get_input():
    return list(map(int,input().split()))

n,qn = get_input()
a = get_input()

sum_list = []

for i in range(32):
    temp = []
    for j in a:
        temp.append((j>>i)&1)
    sum_list.append(list(accumulate(temp)))


for i in range(qn):
    res = 0
    ans = 0
    l,r = get_input()
    l,r = l-1,r-1


    for j in range(32):
        if l==0:
            res = sum_list[j][r]
        else:
            res = sum_list[j][r]-sum_list[j][l-1]
        
        if res>0:
            ans+=1<<j

    print(ans)




