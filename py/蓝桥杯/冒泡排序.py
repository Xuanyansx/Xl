from randomList import rlist


def paixu_v1(L):
    for i in range(len(L)):
        for j in range(L_l):
            if j == L_l-1:
                L_l = L_l-1
                break
            if L[j] > L[j+1]:
                temp = L[j]
                L[j] = L[j+1]
                L[j+1] = temp
                # print(L)


def paixu_v2(L):
    print(len(L))
    for i in range(len(L)-1,-1,-1):
        for j in range(i):
            if L[j]>L[j+1]:
                L[j],L[j+1] = L[j+1],L[j]
            # print(L)
L = rlist()
LL = L.copy()
# L = [3,1,5,6,9,1,3,7,8]
print("L",L)
print("LL",LL)
paixu_v2(L)
print("L",L)
LL.sort()
print("LL",LL)


