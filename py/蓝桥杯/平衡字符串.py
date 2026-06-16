def sn(si):
    if si == 'L':
        return 1
    if si == 'Q':
        return -1

def get_sum_list(s,sl):
    l = [0]*sl
    l[0] = sn(s[0])
    for i in range(1,sl):
        l[i] = sn(s[i])
        l[i] = l[i]+l[i-1]
    return l

def get_sum(i,j,l):
    if i == 0:
        return l[j]
    return l[j]-l[i-1] 


s = input()
sl = len(s)
l = get_sum_list(s,sl)
ans = 0
for i in range(sl):
    for j in range(sl,-1,-1):
        if get_sum(i,j-1,l) == 0 :
            temp = j-i
            if temp>ans:
                ans = temp

print(ans)
