
#十进制转k进制

n = int(input()) 
k = int(input()) #k进制

nums = '0123456789abcdef'

o = ''
while n!=0:
    o += f'{nums[n%k]}'
    n = int(n/k)
print(o[::-1])

















#1 2 4 8 16 32 64 128
#1 2 3 4 05 06 07 008