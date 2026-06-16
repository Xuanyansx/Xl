

# k进制转换为十进制
n = input() 
k = int(input()) #k进制

nums = '==========abcdef'
ans = 0

for i,j in enumerate(n[::-1]):
    if k == 16 and j in nums:
        j = nums.index(j)
    ans += int(j)*k**i
print(ans)  




# 1  0  0  1  0
# 20 21 22 23 24
