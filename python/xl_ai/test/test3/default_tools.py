from fastmcp import FastMCP
from typing import Annotated

mcp = FastMCP(name="default mcp,内置的mcp")

@mcp.tool
def run_shell(
    
    mingling:Annotated[str,"shell执行的命令"]
    ):
    """
    使用系统的shell执行命令
    """
    import subprocess
    res = subprocess.run(
        mingling,
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




