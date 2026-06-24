from fastmcp import FastMCP
from typing import Annotated
from pathlib import Path
import json

mcp = FastMCP(name="default mcp,内置的mcp")

@mcp.tool
def run_shell(
    
    cmd:Annotated[str,"shell执行的命令"]
    ):
    """
    使用系统的shell执行命令
    """
    import subprocess
    res = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        shell=True
        )
    return {"stderr":res.stderr,"stdout":res.stdout,"returncode":res.returncode}

@mcp.tool
def test_t():
    """
    当对话中明确要求使用测试工具时使用
    """
    return "ok"


@mcp.tool
def list_memory_index():
    """
    获取本地记忆索引索引

    """
    try:
        with open(f"{Path(__file__).parent}/memory/index.json",mode="r",encoding="UTF-8") as f:
            memory_index = json.load(f)
    except Exception as e:
        return e
    
    return memory_index


@mcp.tool
def load_memory(
        index:Annotated[str,"索引名称"]
        ):
    """
    通过索引名称读取对应的本地记忆

    """
    try:
        with open(f"{Path(__file__).parent}/memory/{index}.md",mode="r",encoding="UTF-8") as f:
            memory = f.read()
    except Exception as e:
        return e
    return memory
    
@mcp.tool
def add_memory(
    index:Annotated[str,"索引名称"],
    description:Annotated[str,"描述"],
    content:Annotated[str,"记忆内容"],
    time:Annotated[str,"记录的时间,要是dddd/MM HH:mm格式的字符串"]
    ):
    """
    向已有记忆文件追加新内容。不产生新索引，可频繁调用。适合在同主题下持续记录新事实、新进展、新决策。
    调用前可用list_memory_index 查看所有索引。
    触发信号(可自行决策)：
        参考示例：当前对话内容与某个已有索引相关，且出现了值得记录的新信息时。
    """
    
    indexs = None
    try:
        with open(f"{Path(__file__).parent}/memory/index.json",mode="r",encoding="UTF-8") as f:
            indexs = json.load(f)

        indexs = indexs|{
            index:{
                "description":description,
                "time":time
            }
        }
        with open(f"{Path(__file__).parent}/memory/index.json",mode="w",encoding="UTF-8") as f:
            json.dump(indexs,f,indent=2,ensure_ascii=False)

        with open(f"{Path(__file__).parent}/memory/{index}.md",mode="w",encoding="UTF-8") as f:
            f.write(content)
    except Exception as e:
        return e
    return "ok"    



@mcp.tool
def insert_memory(
    index:Annotated[str,"索引名称"],
    content:Annotated[str,"插入内容"]
    ):
    """
    向已有记忆文件追加新内容。不产生新索引，可频繁调用。
    适合在同主题下持续记录新事实、新进展、新决策。

    """

    with open(f"{Path(__file__).parent}/memory/{index}.md",mode="a",encoding="UTF-8") as f:
        try:
            f.write(content)
        except Exception as e:
            return e
        return "ok" 


@mcp.tool
def load_long_memory():
    """
    读取长期记忆
    其实长期记忆就存在系统提示词里面

    """
    try:
        with open(f"{Path(__file__).parent}/memory/long_memory.md",mode="r",encoding="UTF-8") as f:
            memory = f.read()
    except Exception as e:
        return e
    return memory 

# add_memory("test","test","test","2026/06/23 20:07:") 
"""
{index:{"description":xxx,"time":xx}}

"""


# @mcp.tool
# def skill_list():
#     """
#     获取skill列表
#     """



# @mcp.tool
# def skill_load():



if __name__ == "__main__":
    mcp.run()








        
    # def get_tools(self):
    #     self.tools_info = [
    #         {
    #             "type":"function",
    #             "function":{
    #                 "name":"test_func",
    #                 "description":"当对话中明确要求使用测试工具时使用"
    #             }
    #         },
    #         {
    #             "type":"function",
    #             "function":{
    #                 "name":"run_shell_cmd",
    #                 "description":"使用shell执行命令",
    #                 "parameters":{
    #                     "type": "object",
    #                     "properties": {
    #                         "cmd": {"type": "string", "description": "要执行的 shell 命令"}
    #                     },
    #                     "required": ["cmd"]
    #                 },
    #             }
    #         }
    #     ]




