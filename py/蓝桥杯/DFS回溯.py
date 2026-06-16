
def dfs(d):
    if d == n:
        print(path)
        return
    for i in range(n):
        if i in path:
            continue
        path.append(i)
        dfs(d+1)
        path.pop(-1)

   
n = int(input())
path = []
dfs(0)