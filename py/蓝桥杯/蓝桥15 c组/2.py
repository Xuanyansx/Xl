







ans=tt=temp=0
with open('.\log.txt') as f:
    while True:
        s = f.readline().split()
        if not s:
            break
        a,b,t = s
        t = int(t)
        time = t-tt
        tt=t
        if a==b and time<=1000:
            temp+=1
            continue
        if temp>=ans:
            ans = temp
        if temp == 8:
            print(a,b,t)
        temp=1

print(ans)

