

#任意进制的互相转换

nums = '0123456789abcdef'


def shi_to_k(n,k):
    n = int(n)
    k = int(k)
    res = ''
    while n!=0:
        res+=nums[n%k]
        n = int(n/k)
    return res[::-1]


def k_to_shi(n,k):
    n = str(n)
    k = int(k)
    res = 0
    for i,j in enumerate(n[::-1]):
        res+=int(nums.index(j))*k**i
    return res


"""
16 => 10 => 8
"""

while True:
    n = input("输入2 8 10 16进制数,e 退出")
    if n == "e":
        break
    nk = input(f"{n} 是什么进制的")
    k = input("处理成 2 8 10 16 进制")


    res = k_to_shi(n,nk)
    if k == '10':
        print(res)
    else:
        res = shi_to_k(res,k)
        print(res)