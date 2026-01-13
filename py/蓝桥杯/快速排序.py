from randomList import rlist

def v1(L):

    """
    好像意外写出了三路快排wwwwwww
    """
    mid = 0
    rl = []
    ll = []
    if int(len(L)/2) == 0:
        return L
    j = []
    for i in L:
        if L[mid]>i:
            ll.append(i)
        elif L[mid]<i:
            rl.append(i)
        else:
            j.append(i)
    return v1(ll)+j+v1(rl)

def v1_1(L):
    if len(L)<2:
        return L
    p = L[0]
    rl = [i for i in L if i <p]
    pl = [i for i in L if i==p]
    ll = [i for i in L if i>p]
    return v1_1(rl)+pl+v1_1(ll)

def v2(L,left,right):
    j = left
    l = left
    r = right
    if not(left<right):
        return
    while l<r:
        if L[l]>L[r]:
            L[r],L[l] = L[l],L[r]
            j = l^r^j
        if j == l:
            r-=1
        else:
            l+=1
    v2(L,left,l-1)
    v2(L,l+1,right)
    # return L


def v2_1(L,left,right):
    pivot = left
    if not left<right:
        return
    l,r = left,right
    while l<r:
        if L[l]>L[r]:
            L[r] , L[l] = L[l] , L[r]
            j = l^r^j
        if pivot == l:
            r-=1
        else:
            l+=1

def partition(L,left,right):
    pivot = L[left]
    while left<right:
        while left<right and pivot<=L[right]:
            right-=1
        L[left] = L[right]
        while left<right and L[left]<=pivot:
            left+=1
        L[right] = L[left]
    L[left] = pivot
    return left


def v2_2(L,left,right):
    if not left<right:
        return
    mid = partition(L,left,right)
    v2_2(L,left,mid-1)
    v2_2(L,mid+1,right)

            

    




L = rlist()
L = [1,4,5,7,9,10,0]
# L = [1,1,1,1,1,1,1,1,1,1,1,1,1]
# L = [7, 55, 53, 97, 88, 10, 67, 57, 94, 46, 28, 30, 44, 89, 37, 47, 64, 99, 60, 13, 24, 83, 9, 64, 85, 47, 56, 100, 45, 93, 22]
LL = L.copy()

v1_1(L)

"""

3 3 5 0
1 3 5 0

1 3 3 0

[1,2]

[9,6]




"""

