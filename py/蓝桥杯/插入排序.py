from randomList import rlist

def v1(L):
    for i in range(len(L)):
        catch = L[i]
        index = 0
        for j in range(i-1,-1,-1):
            if L[j] > catch:
                L[j+1] = L[j]
            else:
                index = j+1
        L[index] = catch          
L = rlist()
L = [3,1,5,0]
LL = L.copy()

print("L",L)
print("LL",LL)
v1(L)
print("L",L)
LL.sort()
print("LL",LL)
            

"""

3 3 5 0
1 3 5 0

1 3 3 0






"""

