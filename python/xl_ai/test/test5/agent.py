import json
import asyncio
import inspect
from openai import OpenAI
from datetime import datetime
import custom_structs as structs
from xl_mcp.mcp_cs import xlmcp_client
from prompt_toolkit import PromptSession
from typing import Annotated,get_type_hints



class llm:
    def __init__(self,
                api_key,
                base_url,
                message,
                modle = "deepseek-v4-flash"
                ):
        self.modle = modle
        self._message = message
        self._client = OpenAI(
            api_key=api_key,
            base_url=base_url           
        )

    def chat(self,tools,msg):
        client = self._client
        res = client.chat.completions.create(
            model=self.modle,
            tools=tools,
            messages=msg
        )
        self._message.clear()
        return res   



class Todo:
    def __init__(self):
        self.todo_list = {}
        self.todo_data = []


    def create_todo(self,
                    title:Annotated[str,"todo标题"],
                    description:Annotated[str,"描述"],
                    time:Annotated[str,"创建时间yyyy/MM/dd HH:mm格式"]
                    ):
        """
        创建一个todo，然后使用工具往里面添加任务
        
        """
        todo_id = len(self.todo_list)
        todo = structs.Todo(todo_id,title,description,time)
        self.todo_list[todo_id] = todo

    # def add_batch_task(self,
    #                    tasks:Annotated[dict[],"包含task的字典"],
    #                    todo_id
    #                    ):
    #     todo = self.todo_list[todo_id]
    #     todo.tasks


    def get_todo_list(self):
        ...

    def get_tasks(self):
        ...

    def task_done(self,todo_id,task_id):
        ...

    def del_todo(self,todo_id):
        ...
    

class TestTool:
    def __init__(self):
        pass

    def test_t(
        self,
        n: Annotated[int, "一个数字"] = 0
        ):
        """
        当对话中明确要求使用测试工具时使用。
        """
        res = 1
        if n%4 == 0:
            res = 10
        elif n%5 == 0:
            res = 20
        elif str(n)[0] == "7":
            res = 777
        return n+res
    
    def run_shell(
        self,
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




class default_tools:
    def __init__(self):
        self._tools = [
            Todo(),
            TestTool(),
        ]
        self.ctools={}
        self._tool_info = []

        self._TYPE_MAP = {
            "str": "string",
            "int": "integer",
            "float": "number",
            "bool": "boolean",
            "list": "array",
            "dict": "object",
        }
        for i in self._tools:
            for j in inspect.getmembers(i, inspect.ismethod):
                if j[0][0] != '_':
                    self.ctools[j[0]] = j[1]
        for i in list(self.ctools.values()):
            self._tool_info.append(self._get_tool_info(i))



    def _get_tool_info(self, func):
        properties = {}
        required = []
        for i,j in get_type_hints(func,include_extras=True).items():
            properties[i] = {
                "description":j.__metadata__[0],
                "type":self._TYPE_MAP[j.__origin__.__name__]
            }

        for i,j in inspect.signature(func).parameters.items():
            if j.default==inspect.Parameter.empty:
                required.append(i)

        return {
            "type": "function",
            "function": {
                "name": func.__name__,
                "description": inspect.getdoc(func) or "",
                "parameters": {
                    "type": "object",
                    "properties":properties,
                    "required": required,
                    "additionalProperties": False
                }
            }
        }
    
    @property
    def tools(self):
        return self._tool_info


    def tool_call(self,name,args):
        res = "没有这个工具"
        if name in self.ctools:
            res = self.ctools[name](**args)
        return res
    # @staticmethod
    # def get_tools():
    #     ...

class MessageManager:
    def __init__(
            self,
            # message,
            prompt="default",
        ):

        if prompt == "default":
            prompt = "你是一个bot"

        self._sysprompt = {
            "system":prompt
        }

        self._message = []
        self._clean_index = []

    def edit_prompt(self,title,content):
        #没有的title就插入，有的话就是全量替换 2026/07/04 14:37
        self._sysprompt[title] = content


    def get(self):
        temp_prompt = ""

        for i,j in self._sysprompt.items():
            temp_prompt += f"[{i}]\n{j}"

        prompt = [
            {
                "role":"system",
                "content":temp_prompt
            }
        ]
        return prompt+self._message

    def add(self,msg,clean_index=[]):
        self._clean_index.extend(
            (len(self._message) + i,j)
            for i,j in clean_index
        )

        self._message = self._message+msg


    def clear(self):
        if self._clean_index:
            for i,j in self._clean_index:
                self._message[i]["content"] = (
                f"读取完毕，内容删除。如需读取，还请调用{j}加载"
                )
            self._clean_index = []




class FrontendAgent:
    def __init__(
            self,
            api_key,
            tools = [],
            base_url = "https://api.deepseek.com",
            modle = "deepseek-v4-flash"
        ):

        self.modle = modle
        self._message = MessageManager()
        self._tools = tools
        self.default_tools = default_tools()
        self._mcp_client = xlmcp_client()
        self._clean_tools = []
        self._prompt_tool = []
        self._llm = llm(api_key,base_url,self._message)
        self._chat = self._llm.chat

    def _call_tool(self,tool_calls):
        result = []
        # tools_result = []
        clean_tools_index = []
        prompts = []

        for i,tool in enumerate(tool_calls):
            tool_name = tool.function.name
            tool_id = tool.id
            args = tool.function.arguments
            args = json.loads(args)

            if tool_name in self._clean_tools:
                clean_tools_index.append((i,tool_name))

            if tool_name in self.default_tools.ctools:
                res = self.default_tools.tool_call(tool_name,args)
            else:
                res = self._mcp_client.tool_call(tool_name,args)
                
            result.append(
                {
                "role":"tool",
                "tool_call_id":tool_id,
                "content":f"执行结果{res}",
                # "load_tool":flag
                }
            )
            yield {
                    "type":"tool",
                    "body":{
                        "name":tool_name,
                        "args":args,
                        "res":res,
                        "time":datetime.now().strftime("%Y/%m/%d %H:%M")
                    }
                }

        return result,clean_tools_index,prompts


    def send_msg(self,msg):

        tools = self.default_tools.tools+self._tools
        msg = [{
            "role":"user",
            "content":msg
        }]
        self._message.add(msg)

        reply = self._chat(
            tools,self._message.get()
            ).choices[0].message
        
        yield {
                "type":"msg",
                "body":{
                    "msg":reply.content,
                    "think":reply.reasoning_content

                }
            }
        self._message.add([reply])

        while reply.tool_calls:
            tool_res,clean_tools,prompts = yield from (
                self._call_tool(reply.tool_calls)
            )

            self._message.add(tool_res,clean_tools)

            for i in prompts:
                self._message.edit_prompt(**i)

            reply = self._chat(
                tools,self._message.get()
                ).choices[0].message
            
            self._message.add([reply])

            yield (
                {
                    "type":"msg",
                    "body":{
                        "msg":reply.content,
                        "think":reply.reasoning_content
                    }
                }          
            )

        # args = [
        #     {
        #         "type":"tool",
        #         "body":{
        #             "name":toolname,
        #             "args":args,
        #             "res":res,
        #             "time":time
        #         }

        #     }
        # ]

        
        # return res,tres
if __name__ == "__main__":
    ...







# 2026/07/04 12:32: ”前端“和”后端“分离基本实现，现在只需要动run的代码即可实现gui




    
"""

2026/06/29 23:50:
多智能体并行执行这个多todo感觉会有用。我打算我的智能体这样设计：
前台智能体，中间和后台的智能体
前台智能体负责对话和对后台智能体的调度（按任务来），关键决策和执行的命令交由中间中间层智能体审计，
中间层智能体可以选择驳回或是上报给前台智能体让用户定夺，前台智能体主要是负责和用户交互，交互涵盖查询任务进度，任务执行审计。
这样在智能体执行任务时也可以与智能体交互，用户体验更好。

然后是关于智能体的职权分离，前台只负责交互和记录记忆发布任务查询，中间层审计和上报，
后台执行任务调度工具。每一层的智能体所调用的工具是有限的，
比方说前台就只能调用工具来创建任务和启动后台智能体，其他的工具都是没有的

不够这就是后话了，感觉这样设计token会不会消耗的飞快（？
我的最终项目Xl_AI就是打算采用这个逻辑，这个demo我或许会简单实现下，但是中间层可能不会实现（待定

不过我应该会在test6完成这个设计吧，现阶段还是先吧基础的todo完成吧

说起来我的skill的加载还没有完成呢（笑

"""
    

