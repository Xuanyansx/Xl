"""
A 市的车牌由六位组成, 其中前三位可能为数字 0 至 9 , 或者字母 A 至 F
, 每位有 16 种可能。后三位只能是数字 0 至 9。为了减少攀比, 车牌中不能有连 续三位是相同的字符。

例如, 202020 是合法的车牌, AAA202 不是合法的车牌, 因为前三个字 母相同。

请问, A 市有多少个合法的车牌?

4002750
13628160
16467360
16527600
"""

s = [0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F']
s1 = list(range(10))
cp = [0]*6
ans = 0
def dfs(d):
    if d==6:
        flag = True
        for i in range(4):
            temp = cp[i:i+3]
            if len(set(temp))==1:
                flag = False
        if flag:
            global ans
            ans+=1
        return
    
    tmp = s if d>2 else s1
    for i in tmp:
        cp[d] = i
        dfs(d+1)



dfs(0)
print(ans)
