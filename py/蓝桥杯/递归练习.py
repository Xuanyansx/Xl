n = int(input())



# def main(n,m,ans):
#     if m>n/2:
#         return ans
#     ans+=1
#     print(f'{m}'+f'{n}')
#     main(m,1,ans)
#     main(n,m+1,ans)

#     return ans

# ans = main(n,0,0)
# print(ans)


# n = int(input())

# def dfs(n, m):
#     if m > n // 2:
#         return 0
    
#     return 1 + dfs(m, 1) + dfs(n, m + 1)

# print(dfs(n, 0))


ans = 0

def main(n, m):
    global ans
    if m > n // 2:
        return
    ans += 1               # 当前这个数合法
    main(m, 1)             # 继续加
    main(n, m + 1)         # 换下一个数


main(n,0)
print(ans)