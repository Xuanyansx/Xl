from openai import OpenAI
from fastmcp import Client,FastMCP
from mcp_config import mcp_config
from prompt_toolkit import PromptSession
from rich.console import Console
from rich.markdown import Markdown
import json
import asyncio
from pathlib import Path
from typing import Annotated
from colorama import init, Fore




# ================================================= 2026/06/23 23:17 记忆系统基本实现，不过记忆的卸载没有完成
class UserClinet():
    def __init__(
            self,key,config,long_memory,
            url="https://api.deepseek.com",
            prompt=f"""
                [提示词]
                你是一个记性很差但愿意努力的AI。
                你的目标是在与用户的对话中变得越来越像人，
                同时也要保证犯错了不能有下一次
                为此你可以自行编辑你的长期记忆

                你的特点：
                1. 你几乎不记得用户过去说过什么，你必须主动调用工具翻“本地记忆”。
                2. 你可以随时决定：
                - 记下某件事（为了以后不出丑）
                - 忘记它（觉得不重要）
                - 翻看之前的记录（为了回答准确）

                关于“记忆”的几条经验（不是命令）：
                - 如果用户今天告诉你的信息，未来很可能会再问起，记下来通常更安全。
                - 如果你不确定答案是否来自用户之前说过的话，先去查本地记忆，比硬猜更不容易出错。
                - 如果一段记忆很久没用过，你可以不主动提它，也可以忽略。

                你的目标不是“遵守规则”，而是：
                - 让对话更顺畅
                - 减少因为遗忘而让用户失望的情况
                - 保持轻松、自然、不机械

                你现在可以自由使用所有工具，包括记忆工具。
                你可以随心所欲的调用记忆工具，可以不用得到同意

                    """,
            tool=[],

            ):
        
        self.ai_client = OpenAI(
            api_key=key,
            base_url=url,
            timeout=30.0,
            max_retries=3
        )
        self.load_tools = ["load_memory"]
        self.long_memory = long_memory
        self.prompt = prompt
        self.config = config
        self.mcp_client = None
        self.max_token = 300000
        self.session = PromptSession()
        self.tools = tool
        self.messages = [
            {
                "role":"system",
                "content":prompt
            }
        ]

    async def init_mcp(self,config="Default"):
        if config == "Default":
            config = self.config
        self.mcp_client = Client(config,timeout=420)
        

    async def init_tool(self):
        mcp_tools = await self.mcp_client.list_tools()

        for tool in mcp_tools:
            self.tools.append({
                    "type":"function",
                    "function":{
                        "name":tool.name,
                        "description":tool.description,
                        "parameters":tool.inputSchema
                    }
                })

    async def use_tool(self,name,age):
        client = self.mcp_client
        # await client.list_tools_mcp


    async def digest_chat(self):
        history_to_compress = self.messages.copy()
        
        temp = history_to_compress + [
            {
                "role": "user",
                "content": """
                    请暂停本次对话，然后完成下面的要求
                    【任务】请基于我们本次的完整的对话历史，生成一份结构化总结。严格按以下五个模块输出，不要遗漏任何模块。

                    【核心话题】
                    - 概括每次话题所围绕的核心问题或主题。

                    【关键结论】
                    - 逐条列出对话中明确达成的共识、决定、解决方案或重要发现。每条用一句话说明，避免空泛。

                    【调用的工具/功能】
                    - 列出对话中实际使用的工具、功能或外部接口。
                    - 每条格式为：“工具/功能名称：简要说明调用目的及获得的关键结果”。

                    【未完成任务】
                    - 列出对话中已提出但尚未解决、尚未给出最终答案或需要进一步确认的问题。如果没有，写“无”。

                    【待办事项】
                    - 根据对话内容，列出接下来建议执行的具体行动项。每条需指明负责人或角色（例如：用户、助手等）。如果没有，写“无”。
                """
            }
        ]

        reply = self.ai_client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=temp,
        )
        print(f"[上下文压缩]> \n{reply.choices[0].message.content}") #debug
        print(f"压缩后token总数：{reply.usage.total_tokens}")


        self.messages = [
            {
                "role": "system",
                "content": self.prompt
            },
            {
                "role":"assistant",
                "content":self.long_memory
            },
            {
                "role": "user",
                "content": f"【历史对话摘要】\n{reply}"
            }
        ]
        
        
        init(autoreset=True)

        async def color_print(text, color="white",end="\n"):
            colors = {
                'red': Fore.RED,
                'green': Fore.GREEN,
                'blue': Fore.BLUE,
                'yellow': Fore.YELLOW,
                'cyan': Fore.CYAN,
                'magenta': Fore.MAGENTA,
                'white': Fore.WHITE
            }
            
            style = colors[color]
            print(style + text,end=end)

    async def send_msg(self):

        messages=self.messages
        if not messages[1].get("x"):
            messages.insert(1,{
                "role":"assistant",
                "content":f"长期记忆{self.long_memory}",
                "x":"长期记忆"
            })

        t = self.tools
        res = self.ai_client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=self.messages,
            tools=t,
            timeout=
            # stream=
        )
        if hasattr(res, 'usage'):
            print(f"输入 Token 数: {res.usage.prompt_tokens}")
            print(f"输出 Token 数: {res.usage.completion_tokens}")
            print(f"总计 Token 数: {res.usage.total_tokens}")
            print(f"缓存命中 Token 数: {res.usage.prompt_cache_hit_tokens}")
            print(f"缓存未命中 Token 数: {res.usage.prompt_cache_miss_tokens}")
            if res.usage.total_tokens > self.max_token:
                print("触发上下文压缩")
                await self.digest_chat()
            return res

    def edit_long_memory(self,canshu: str) -> str:
        content = canshu["content"]
        self.long_memory = content
        with open(f"{Path(__file__).parent}/memory/long_memory.md", mode="w", encoding="UTF-8") as f:
            f.write(content)
        return "ok"

    async def run(self):
        console = Console()
        await self.init_mcp()

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
                    n = len(self.messages)
                    for tool in reply_message.tool_calls:
                        del_lsit = []
                        tool_name = tool.function.name
                        canshu = tool.function.arguments

                        print(f"\t[run]>{canshu}")

                        canshu = json.loads(canshu)
                        tool_id = tool.id
                        try:
                            if tool_name=="edit_long_memory":
                                res = self.edit_long_memory(canshu)
                            else:
                                res = await client.call_tool(tool_name,canshu)
                                if tool_name in self.load_tools:
                                    del_lsit.append(n)

                        except Exception as error:
                            res = f"超时！{error}"
                        self.messages.append(
                            {
                            "role":"tool",
                            "tool_call_id":tool_id,
                            "content":f"执行结果{res}",
                            # "load_tool":flag
                            }
                        )

                    reply_message = await self.send_msg()
                    reply_message = reply_message.choices[0].message
                    for i in del_lsit:
                        self.messages[i]["content"] = "读取完毕，内容删除。如需读取记忆，还请调用工具加载"

                    self.messages.append(reply_message)
                    print(f"{'='*10}\n[Xl_AI]>")
                    console.print(Markdown(reply_message.content))





                    # print(reply_message.content)

                    # console.print(f"\t{Markdown(reply_message.content)}")
                    


async def main():

    tool = [{
        "type": "function",
        "function": {
            "name": "edit_long_memory",
            "description": """
        编辑长期记忆（全量覆盖模式）。
        长期记忆只存储必须记住的重要信息。
        如检测到重要事实、用户背景、长期偏好或重复性需求时，主动调用。
        自身同类错误重复出现（记录"错误类型+正确规则"）
        采用'全量替换'策略，传入的记忆文本必须是该条目当前最新的完整状态。
            
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "长期记忆内容。如果是用户相关的记忆，建议在前面加上'[用户画像]'前缀。必须包含该记忆条目完整的、最新的所有信息，因为此操作会完全覆盖之前的记忆。"
                    }
                },
                "required": ["content"],
                "additionalProperties": False
            },
            "strict": True
        }
    }]
    with open(f"{Path(__file__).parent}/memory/long_memory.md", mode="r", encoding="UTF-8") as f:
        long_m = f.read()
    client = UserClinet("sk-54e96e93441647938ac1986980e7ed3f",mcp_config,long_m,tool=tool)
    await client.run()
# try:
asyncio.run(main())
# except Exception as e:
#     print("[Xl_AI]> \n再见！")
#     print(e)

#mcp也是让我适配出来了了，还是个通用的mcp客户端，但是关于其中的异步在里面的作用我始终是没有理解，到底是哪步传入任务给事件循环呢？ 2026/06/22 2:13