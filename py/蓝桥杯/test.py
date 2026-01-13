# for i in range(1,10):
#     for j in range(1,i+1):
#         print(f"{i}*{j}={i*j}",end=" ")
#     print("++")



# a = [1]
# b = []
# print(int(len(a)/2)==0)


# from randomList import rlist

# def shuang_zhi_zheng(l,n):
#     print(id(l))
#     if n <=0:
#         return
#     n-=1
#     return shuang_zhi_zheng(l,n)


# i,j = map(int,input().split())

# print(type(i))


# def inter():
#     while True:
#         for i in [2,0,2,5]:
#             yield i

# # get_i = inter()

# # for i in range(h):
# #     for j in range(w):
# #         print(next(get_i),end='')
# #     print()

# a = [1,2,3,4,5]
# print(a[1:])

# h,w = map(int,input().split())

# def inter():
#     while True:
#         for i in [2,0,2,5]:
#             yield i

# get_i = inter()

# for i in range(h):
#     for j in range(w):
#         print(next(get_i),end='')
#     print()

# h,w = map(int,input().split())

# for i in range(h):
#     i = i%4
#     for j in range(w):
#         print("2025"[(j+i)%4],end="")
#     print()


# def a():
#     print(1)

# def b():
#     a()

# def a():
#     print(2)
    
# def c():
#     a()

# b()
# c()


# rl = [1]
# ll = [2,4,6,8,10] 
# temp = []

# temp+=rl[(len(rl)-len(ll))+1:]
# print(temp)

# mid = int(len(rl)/2)
# print(rl[:mid+1])
# print(rl[mid:])

# ll = [1,3,5,7,9,22]
# rl = [2,4,6,8,10,11,12,13]

# temp = []

# while ll and rl:
#     while ll and ll[0]<=rl[0]:
#         temp.append(ll.pop(0))
#     while rl and rl[0]<=ll[0]:
#         temp.append(rl.pop(0))
# else:
#     if ll:
#         temp+=ll
#     if rl:
#         temp+=rl

# print(temp)
# L = [1,2,3,4,5,6,7,8,9]
# mid = int(len(L)/2)
# print(L[mid:])
# print(L[:mid])
# print(mid)


# n = int(input())
# ans = n

# while n>1:

#     if n % 2 == 0:
#         n=int(n/2)
#     else:
#         n = int(n*3+1)
#     if ans<n:
#         ans = n
# print(ans)

# n = int(input())
# n = 10
# ans = 0
# for i in range(2,n+1):
#     res = i
#     while res>1:
#         if res%2==0:
#             res = res//2
#         else:
#             res = res*3+1
#         if res < i:
#             continue
#         if res>ans:
#             ans=res
# print(ans)

s = ['.','G','.','.']