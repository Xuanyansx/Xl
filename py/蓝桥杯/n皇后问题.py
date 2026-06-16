
class new_list(list):
    def get(self,index,res=None):
        try:
            res = self[index]
        except:
            pass
        return res

def dfs(d):
    if d == n:
        global ans
        ans+=1
        return
    
    for i in range(n):
        flag = False
        for j in range(1,d+1):
            temp = path.get(d-j)
            if temp!=None and (temp==i+j or temp == i-j):
                flag = True
                break

        if i in path or flag:
            continue
        path.append(i)
        dfs(d+1)
        path.pop(-1)


n = int(input())
# n = 2
path = new_list([])
ans = 0
dfs(0)
print(ans)





""""




[0, 2, 4, 1, 3] 1
[0, 3, 1, 4, 2] 2
[1, 4, 2, 0, 3] 3
[2, 0, 3, 1, 4] 4
[3, 0, 1, 4, 2] 5
[3, 0, 2, 4, 1] 6
[4, 1, 3, 0, 2] 7
[4, 2, 0, 1, 3] 8
[4, 2, 0, 3, 1] 9

[0, 2, 4, 1, 3] 1
[0, 3, 1, 4, 2] 2
[1, 4, 2, 0, 3] 4
[2, 4, 0, 3, 1] 6
[2, 4, 1, 3, 0] 7
[3, 0, 2, 4, 1] 8
[3, 1, 4, 2, 0] 9
[4, 1, 3, 0, 2] 10
[4, 2, 0, 3, 1] 11

"""