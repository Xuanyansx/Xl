from openai import OpenAI
from fastmcp import Client
from test.test4.mcp_config import mcp_config
from prompt_toolkit import PromptSession
from rich.console import Console
from rich.markdown import Markdown
import json
import asyncio
import subprocess, os

class UserClinet():
    def __init__(
            self,key,config,
            url="https://api.deepseek.com",
            prompt=" 你是xlai"
            ):
        
        self.ai_client = OpenAI(
            api_key=key,
            base_url=url
        )
        self.mcp_client = Client(config,timeout=420)
        self.session = PromptSession()
        self.tools = []
        self.messages = [
            {
                "role":"system",
                "content":prompt
            }
        ]

    async def init_tool(self):
        client = self.mcp_client
        mcp_tools = await client.list_tools()

        server_names = list(mcp_config["mcpServers"].keys())
        loaded = set()
        for t in mcp_tools:
            prefix = t.name.split("_")[0] if "_" in t.name else t.name
            loaded.add(prefix)
            # 我知道这非常不优雅，但是我也只能通过这个方式获取本地加载的服务了   2026/06/22 12:12

        failed = [s 
                  for s in server_names 
                  if s not in loaded
                  ]
        if failed:
            print(f"[Xl_AI] MCP 服务加载失败: {', '.join(failed)}，清理残余进程...")
            for _ in range(3):  
                subprocess.run(["pkill", "-P", str(os.getpid())])
                import time
                time.sleep(0.5)

        for tool in mcp_tools:
            self.tools.append({...})
            for tool in mcp_tools:
                self.tools.append({
                    "type":"function",
                    "function":{
                        "name":tool.name,
                        "description":tool.description,
                        "parameters":tool.inputSchema
                    }
                })


    async def send_msg(self):
        t = self.tools
        res = self.ai_client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=self.messages,
            tools=t
        )
        if hasattr(res, 'usage'):
            print(f"输入 Token 数: {res.usage.prompt_tokens}")
            print(f"输出 Token 数: {res.usage.completion_tokens}")
            print(f"总计 Token 数: {res.usage.total_tokens}")
            print(f"缓存命中 Token 数: {res.usage.prompt_cache_hit_tokens}")
            print(f"缓存未命中 Token 数: {res.usage.prompt_cache_miss_tokens}")
            return res

    async def run(self):
        console = Console()
        client = self.mcp_client

        async with client:
            await self.init_tool()
            while True:
                user_input = await self.session.prompt_async("[Xl_AI]< ")
                if user_input in ["exit","q","quit"]:
                    print("[Xl_AI]> \n再见！")
                    break
                user_msg = {
                    "role":"user",
                    "content":user_input
                }
                self.messages.append(user_msg)
                reply = await self.send_msg()

                reply_message = reply.choices[0].message
                self.messages.append(reply_message)
                print(f"{'='*10}\n[Xl_AI]>")
                console.print(Markdown(reply_message.content))
                # print(reply_message.content)

                while reply_message.tool_calls:
                    for tool in reply_message.tool_calls:
                        
                        tool_name = tool.function.name
                        canshu = tool.function.arguments
                        print(f"\t[run]>{canshu}")
                        canshu = json.loads(canshu)
                        tool_id = tool.id
                        try:
                            res = await client.call_tool(tool_name,canshu)
                        except Exception as error:
                            res = f"超时！{error}"
                        self.messages.append(
                            {
                            "role":"tool",
                            "tool_call_id":tool_id,
                            "content":f"执行结果{res}"
                            }
                        )
                    reply_message = await self.send_msg()
                    reply_message = reply_message.choices[0].message
                    self.messages.append(reply_message)

                    print(f"{'='*10}\n[Xl_AI]>")
                    console.print(Markdown(reply_message.content))
                    # print(reply_message.content)

                    # console.print(f"\t{Markdown(reply_message.content)}")
                    
        

async def main():

    client = UserClinet("sk-54e96e93441647938ac1986980e7ed3f",mcp_config)
    await client.run()
try:
    asyncio.run(main())
except Exception as e:
    print("[Xl_AI]> \n再见！")
    print(e)


#mcp也是让我适配出来了了，还是个通用的mcp客户端，但是关于其中的异步在里面的作用我始终是没有理解，到底是哪步传入任务给事件循环呢？ 2026/06/22 2:13