
def px(a,left=None,right=None):
    if left==right==None:
        left = 0
        right = len(a)-1
    poit = left
    l = left
    r = right
    
    if not(left<right):
        return
    
    while left<right:
        if a[left]>a[right]:
            a[left],a[right] = a[right],a[left]
            if left == poit:
                poit = right
            else:
                poit = left
        if left==poit:
            right-=1
        else:
            left+=1

    px(a,l,right-1)
    px(a,left+1,r)




def v2(L,left=None,right=None):
    if left==right==None:
        left = 0
        right = len(a)-1
    poit = left
    l = left
    r = right

    if not(left<right):
        return
    
    while l<r:
        if L[l]>L[r]:
            L[r],L[l] = L[l],L[r]
            poit = l^r^poit
        if poit == l:
            r-=1
        else:
            l+=1
    v2(L,left,l-1)
    v2(L,l+1,right)

a = [1,6,7,8,4,9,1,3,8]

px(a)
print(a)