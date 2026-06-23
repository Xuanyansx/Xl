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
    time:Annotated[str,"记录的时间,要是dddd/mm格式的字符串"]
    ):
    """
     添加一条本地记忆。本地记忆存储在外部文件中，
     本地记忆是非常低廉的，只要是你觉得应该要记忆的即可调用工具存储                                                                                                                          
     不会自动加载到对话中，需要通过 list_memory_index 查看目录，                                                                                                           
     通过 load_memory 按需读取。                                                                                                                                           
                                                                                                                                                                           
     适合存储的内容：(仅为建议，参考即可)                                                                                                                                                      
     - 项目文档、设计方案、代码片段                                                                                                                                        
     - 历史对话的详细摘要                                                                                                                                                  
     - 外部资料、研究笔记                                                                                                                                                  
     - 用户交代的长期任务及其进度

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
    往现的某段记忆中插入内容
    """

    with open(f"{Path(__file__).parent}/memory/{index}.md",mode="a",encoding="UTF-8") as f:
        try:
            f.write(content)
        except Exception as e:
            return e
        return "ok" 


@mcp.tool
def load_memory(
        index:Annotated[str,"索引名称"]
        ):
    """
    读取长期记忆
    其实长期记忆就存在系统提示词里面

    """
    try:
        with open(f"{Path(__file__).parent}/memory/{index}.md",mode="r",encoding="UTF-8") as f:
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




