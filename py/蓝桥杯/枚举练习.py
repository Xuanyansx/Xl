



"""

扫雷

"""


# def input_list():
#     return list(map(int,input().split()))

# n,m = input_list()

# map_data = []

# for i in range(n):
#     map_data.append(input_list())

# game_map = [ [0] * m for _ in range(n) ]

# des = [(0,1),(0,-1),(-1,0),(1,0),(-1,-1),(-1,1),(1,-1),(1,1)]

# print()

# for i in range(n):
#     for j in range(m):
#         if map_data[i][j] == 1:
#             game_map[i][j] = 9
#         else :
#             game_map[i][j] = 0
#             for d in range(8):
#                 x = i + des[d][0]
#                 y = j + des[d][1]
#                 if n>x>=0 and m>y>=0:
#                     game_map[i][j]+=map_data[x][y]

#         print(game_map[i][j],end=" ")
#     print()


"""
n 瓶奶，三个瓶盖可换一瓶奶，如此循环

"""

# n = int(input())

# m = n
# while n>2:
#     if n>3:
#         n-=2
#         m+=1
# print(m)
2/=1

