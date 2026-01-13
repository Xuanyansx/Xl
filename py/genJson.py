import simplejson as json
import re
import os
from tqdm import tqdm  # 导入tqdm

"""
2023/12/25

让ai写了一个处理文本的，没想到没有达到预期，，，，

不能偷懒了..114514
然后自己写了个，没想到比ai的还精简....

"""
def textTOjson(texts):
    jsonList = []
    groupJson = {}
    List = []
    matches = []
    tempList = []
    Bool = False
        # 正则提取需要的部分
    # pattern = re.compile(r'\n(\d+)(.*?)\nA\.(.*?)\nB\.(.*?)\nC\.(.*?)(?:\nD\.(.*?))?\n参考答案:(.*?)\n解析:(.*?)(?=\d+\.|$)', re.DOTALL)
    # matches = pattern.findall(text)
    for i in tqdm(texts , desc="处理数据ing...",unit = "字符串"):
        if (i[0] in range(10)) and (i[1]=="."):
            Bool = True
        if Bool:
            tempList.append(i)
            
        if (i[0] in ['A','B','C','D']) and (i[1]=='.'):
            pass
    

    for i, m in enumerate(tqdm(matches, desc="处理文本ing...", unit="题目")):
        group = i // 50  # 组id
        groupId = i % 50  # 组内id
        groupJson[groupId] = {
            'group': group,  # 添加组号
            'groupId': groupId,  # 添加组内ID
            'question': m[1].strip(),  # 题目
            'options': [
                [m[2].strip()],  # 选项 A
                [m[3].strip()],  # 选项 B
                [m[4].strip()],  # 选项 C
                [m[5].strip()]   # 选项 D
            ],
            'answer': m[6].strip(),  # 答案
            'explanation': m[7].strip(),  # 解析
            'occurrences': 0,  # 初始出现次数为0
            'errors': 0  # 初始出错次数为0
        }

        if groupId == 49:
            jsonList.append(groupJson)
            groupJson = {}
            List.append([group,None])
    if groupJson:
        jsonList.append(groupJson)
        List.append([group,None])
        try:
            os.makedirs("data")  # 创建文件夹
        except:
            pass
    with open(f"data/stats.json",mode="w",encoding="UTF-8") as f:
        json.dump({"groupNum":group,"lastG":groupId},f)
    with open("data/qStatus.json",mode="w",encoding="UTF-8") as f:
        json.dump({"status":List},f)
    return group + 1, jsonList

def generateJson(File):
    with open(File, mode="r", encoding="UTF-8") as b:
        texts = b.readlines()
    groupNum, groupJson = textTOjson(texts)
    print("\n")
    for i in tqdm(range(groupNum), desc="创建文件ing...", unit="组"):
        with open(f"data/{i}.json", mode="w", encoding="UTF-8") as f:
            json.dump(groupJson[i], f)
        


while True:
    File = input("输入程序路径 (或输入 'n' 退出): ")
    if not (os.path.exists(File)):
        print("未找到此文件")
        continue
    if File.lower() == 'n':
        break

    generateJson(File)

    if input("程序处理成功! 点击回车继续，输入 'n' 退出: ") == 'n':
        break
    

