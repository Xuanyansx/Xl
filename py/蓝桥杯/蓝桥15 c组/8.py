
n = int(input())

s = ['l','q','b']

for i in range(n):
    temp = ''
    s2 = input()
    for i in range(len(s2)-1,-1,-1):
        if s2[i] not in s:
            break
        temp+=s2[i]
    temp+=s2
    if temp == temp[::-1]:
        print("Yes")
    else:
        print("No")


