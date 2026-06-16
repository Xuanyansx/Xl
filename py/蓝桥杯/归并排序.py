from randomList import rlist


def v1(L):
    mid = int(len(L)/2)
    if not mid:
        return L
    temp = []
    left_l = L[:mid]
    right_l = L[mid:]

    ll = v1(left_l)
    rl = v1(right_l)

    while ll and rl:
        while ll and rl and ll[0]<=rl[0]:
            temp.append(ll.pop(0))
        while rl and ll and rl[0]<=ll[0]:
            temp.append(rl.pop(0))
    else:
        if ll:
            temp+=ll
        if rl:
            temp+=rl
    return temp
        

def v2(L):
    mid = int(len(L)/2)
    if not mid:
        return L
    temp = []
    left_l = L[:mid]
    right_l = L[mid:]

    left_l = v1(left_l)
    right_l = v1(right_l)

    l = r = 0

    while l<len(left_l) and r<len(right_l):
        if left_l[l]<=right_l[r]:
            temp.append(left_l[l])
            l+=1
        else:
            temp.append(right_l[r])
            r+=1
    temp+=left_l[l:]+right_l[r:]
    return temp


        
        


L = rlist()
# L = [3,1,5,6,9,1,3,7,8]
# L = [1,1,1,1,1,1,1]
LL = L.copy()
print("L",L)
print("LL",LL)
L = v2(L)
print("9L",L)
LL.sort()
print("LL",LL)


