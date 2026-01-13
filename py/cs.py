# import tkinter as tk

# def print_values():
#     for i, var in enumerate(vars):
#         print(f'Button {i}: {var.get()}')

# def clear_values():
#     for var in vars:
#         var.set(0)

# root = tk.Tk()

# vars = []
# for i in range(10):
#     var = tk.IntVar()
#     chk = tk.Checkbutton(root, text=str(i), variable=var)
#     chk.pack(side=tk.LEFT)
#     vars.append(var)

# print_button = tk.Button(root, text='Print values', command=print_values)
# print_button.pack()

# clear_button = tk.Button(root, text='Clear values', command=clear_values)
# clear_button.pack()

# root.mainloop()

# import re

# # 定义正则表达式
# pattern = re.compile(r'(\d+)\.(.*?)\nA\.(.*?)\nB\.(.*?)\nC\.(.*?)\nD\.(.*?)\n参考答案:(.*?)\n解析:(.*?)(?:\n|\Z)', re.DOTALL)



# # 定义示例文本
# text = """
# 1.根据我国法律法规,下列情形不属于工伤的是()[1分]
# A.小樊在上班时由于操作不符合规程,手指被 机器绞伤
# B.小王在下班回家的路上被一辆闯红灯的轿车 撞伤
# C.老张在上班操作吊车时突发心脏病当场死亡
# 参考答案:D
# 解析:职工有故意犯罪、醉酒或吸毒、自残或自杀情形的不得认定为工伤或视同工伤。
# 2.甲在珠宝店柜台前试戴一条价值8000元的金项链,趁营业员不注意,用一条假的同款式项链 调包,然后称不满意项链款式,扬长而去。甲的 行为构成 ()[1分]
# A.诈骗罪
# B.抢夺罪
# C.盗窃罪
# D.侵占罪
# 参考答案:C
# 解析:诈骗罪指以非法占有为目的,虚构事实、隐瞒真相骗取数额较大财物的行为;抢夺罪 是指直接夺取或多次夺取;盗窃罪指窃取数额 较大或盗窃、扒窃行为,题中“以假换真”行为属 于盗窃;侵占罪指将代为保管的他人财物非法 占为己有。
# 3.我国古代《唐律》对六种非法获取公私财物的犯罪进行了规定,即为“六赃”。下列选项不属于“六赃”的是  ()[1分]
# A.受财枉法
# B.玩忽职守
# C.受财不枉法
# D.强盗
# 参考答案:B
# 解析:六赃:受财枉法、受财不枉法、受所监 临财物、强盗、盗窃和坐赃。
# """

# # 使用正则表达式匹配文本
# matches = re.findall(pattern, text)
# print(matches)
import simplejson as json
import re
F = input(">>>")

with open(F,mode='r',encoding="UTF-8") as f:
    data = f.read()
pattern = re.compile(r'(\d+)\.(.*?)\nA\.(.*?)\nB\.(.*?)\nC\.(.*?)(?:\nD\.(.*?))?\n参考答案:(.*?)\n解析:(.*?)(?:\d+\.)', re.DOTALL)
pattern = re.compile(r'(\d+)\.(.*?)\nA\.(.*?)\nB\.(.*?)\nC\.(.*?)(?:\nD\.(.*?))?\n参考答案:(.*?)\n解析:(.*?)(?=\d+\.|$)', re.DOTALL)

matches = pattern.findall(data)

print(matches)
i = input()
    
    








