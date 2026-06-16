s1 = list(input())
s2 = list(input())

ans = 0


s1_l = len(s1)

for i in range(s1_l):
    if s1[i] != s2[i]:
        ans+=1
        s1[i] = s2[i]
        if s1[i+1] == 'o':
            s1[i+1] = '*'
            continue
        s1[i+1] = 'o'
print(ans)