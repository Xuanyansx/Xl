
a,b,c,d = list(map(int,input().split()))


flag = True

while True:
    if a <= 0:
        print("QIAO")
        break
    if c <= 0:
        print("LAN")
        break
    if flag:
        c = c-b
    else:
        a = a-d

    flag = not flag
        