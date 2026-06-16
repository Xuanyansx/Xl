from randomList import rlist

def v1(L):
    for i in range(len(L)):
        for j in range(i,len(L)):
            if L[i] > L[j]:
                L[i],L[j] = L[j],L[i]

def v2(L):
    for i in range(len(L)):
        x = L[i]
        xi = i
        for j in range(i+1,len(L)):
            if L[j] < x:
                x = L[j]
                xi = j
        L[i],L[xi] = L[xi],L[i]
        
        
def v3(L):
    for i in range(len(L)):
        xi = i
        for j in range(i+1,len(L)):
            if L[j] < L[xi]:
                xi = j
        L[i],L[xi] = L[xi],L[i]         


L = rlist()
# L = [3,1,5,6,9,1,3,7,8,0]
LL = L.copy()

print("L",L)
print("LL",LL)
v3(L)
print("L",L)
LL.sort()
print("LL",LL)


