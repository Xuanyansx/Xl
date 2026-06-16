import unicodedata

def convert_fullwidth_to_halfwidth(txt):
    return ''.join([unicodedata.normalize('NFKC', char) for char in txt])

# 获取用户输入的文件路径
file_path = input("请输入文件的路径：")

# 读取文件
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 转换全角符号为半角符号
converted_content = convert_fullwidth_to_halfwidth(content)

# 将转换后的内容写回文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(converted_content)
