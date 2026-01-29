
import keyboard as kb

def select_menu(text:str,opt:list,res=0):
    """
    返回一个res 1 代表选项1
    text 提示信息
    opt:[
    选项1，
    选项2，
    ...
    ]
    res=0 默认选择 值为0代表不选择任何 
    """
    print(f"<= {text} =>")
    

    