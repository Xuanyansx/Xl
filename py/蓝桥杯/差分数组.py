





"""
1 2 3 4 5 6 7
1 1 1 1 1 1 1
(1,3)
1 2 1 1 1 1 1
1 3 4 5 6 7 8
1 2 1 1 0 1 1
1 3 4 5



"""

def get_input():
    return list(map(int,input().split()))

def get_diff(a,n):
    l = []
    l.append(a[0])
    for i in range(1,n):
        l.append(a[i]-a[i-1])
    return l

def get_sum(a:list,n):
    for i in range(1,n):
        a[i] = a[i-1]+a[i]
    s = " ".join(map(str,a))
    return s

s = ""
while True:
    try:
        n,m = get_input()
    except:
        break
    a = get_input()
    al = get_diff(a,n)

    for i in range(m):
        x,y,z = get_input()
        al[x-1] +=z
        if y!=n:
            al[y]-=z
    s+= get_sum(al,n)+"\n"
    
print(s)



