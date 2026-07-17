import json
import asyncio
import inspect
from openai import OpenAI
from datetime import datetime
from pydantic import BaseModel
import custom_structs as structs
from xl_mcp.mcp_cs import xlmcp_client
from prompt_toolkit import PromptSession
from typing import Annotated,Literal,get_type_hints




class llm:
    def __init__(self,
                api_key,
                base_url,
                modle = "deepseek-v4-flash"
                ):
        self.modle = modle
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
        # print(msg)
        return res   


class Todo:
    def __init__(self):
        self._todo_list = {}

    # def save_task_output(self,):
    #     ...

    def create_todo(self,
                    title:Annotated[str,"todo标题"],
                    description:Annotated[str,"描述"],
                    ):
        """
        create_todo 工具说明：
        - 请先对目标进行评估，然后再创建todo和规划任务
        - 然后使用submit_tasks往里面添加任务列表
        - 适用场景举例：
        a) 明确的多步骤任务（如"先A再B然后C"）
        b) 探索性研究任务（可以先规划探索方向/测试用例分组）
        c) 需要在多个工具间切换协作的任务
        - 注意：即使任务是探索性的、结果不确定的，也建议先创建todo来规划大致的步骤框架
        
        """
        time = datetime.now().strftime("%Y/%m/%d %H:%M")
        todo_id = len(self._todo_list)
        todo = structs.Todo(todo_id,title,description,time)
        self._todo_list[f'{todo_id}'] = todo
        return f"ok id:{todo_id}"

    def submit_tasks(self,
                    tasks:Annotated[structs.ttttt,
                    "包含task的列表,任务按下标顺序来"],
                    todo_id:Annotated[str,"目标todo的id"]
                    ):
        """
        往todo提交任务列表（必须是一次性提交
        任务数量必须大于2
        """
        todo = self._todo_list[todo_id]
        # res = {
        #     "title":todo.title
        # }
        content = ""
        for i in tasks['todos']:
            todo.add_task(i["description"],i["content"])
            content+=f"[]"
        return todo

    def start_todo(self,
                   todo_id:Annotated[str,"指定的todo的id"]
                   ):
        """
        开始完成指定todo的任务，在此之前你必须添加任务
        """

        res = structs.TodoRes()

        todo:structs.Todo = self._todo_list[todo_id]
        tasks = todo.tasks

        if tasks == {}:
            res.res = "任务列表没有任务"
        else:
            work_prompt = f"""
            当前任务: 任务id{tasks[0].id} 任务目标{tasks[0].description}
            任务描述：{tasks[0].content}

            下一个任务: 
                任务id{tasks[1].id} 任务目标{tasks[1].description}

            """

            res.res = "ok"
            res.work_prompt = work_prompt
        # res.turn = True


        return res

    def update_task_status(self,
                           todo_id:Annotated[str,"todo的id"],
                           status: Literal['done','failed'],
                           task_result:Annotated[str,"本次任务产生的关键数据和可能对下一个任务有用的数据，没有的话可以填个无。/" \
                           "因为任务执行过程和执行结果多会被清楚，所以这里你必须写清楚当前这个任务产生些什么结论和关键的数据"]
                            ):
        """
        更新当前任务的状态，调用这个工具代表当前任务已经成功或是失败了
        更新完成后如果还有任务程序会自动给你委派新的任务
        请总结这次任务的冠军数据和结论！然后传递给task_result

        
        """

        res = structs.TodoRes()

        todo:structs.Todo = self._todo_list[todo_id]
        tasks = todo.tasks
        running_task_id = todo.running_task_id
        next_task_id = running_task_id+1

        tasks[running_task_id].status = status

        todo.running_task_id = next_task_id
        todo.task_result.append(task_result)

        if next_task_id >= len(tasks):
            work_prompt = f"""
            你完成了这个todo，工作记录全部都已删除，
            只会保留任务产生的关键数据和结论
            请向用户报告当前的情况和任务状态
            """ 
            for i in tasks:
                work_prompt+=f"""
                任务产生的关键结论和数据：
                {todo.task_result}

                任务完成情况
                {tasks[i].description} {tasks[i].status}
                """
            todo.status = "done"
            res.done = "True"

        else:
            next_task_p = "无"
            if next_task_id+1<len(tasks):
                next_task_p = f"任务id {next_task_id+1} 任务描述 {tasks[next_task_id+1].description}"
            work_prompt = f"""
            任务{tasks[running_task_id].id} {tasks[running_task_id].status}
            前面任务的执行痕迹以删除只保留了关键的数据和结论
            之前任务产生的关键数据和结论：
            {todo.task_result}
            ====
            先你需要完成
                任务id{next_task_id}
                任务主题{tasks[next_task_id].description}
                任务描述{tasks[next_task_id].content}

            
            下一个任务：
                {next_task_p}
            """

        res.res = "ok"
        res.work_prompt = work_prompt
        res.todo = todo
        # res.turn = True

        return res



    

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
        self.clear_tools = []

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
                    self.ctools[j[0]] = (j[1],i)

        for i,j in list(self.ctools.values()):
            if i.__name__[-1] == "C":
                self.clear_tools.append(i)
            self._tool_info.append(self._get_tool_info(i,j.__class__.__name__))


    def _get_tool_info(self, func, class_name):
        def _resolve_refs(node, defs):
            if isinstance(node, dict):
                if '$ref' in node:
                    key = node['$ref'].split('/')[-1]
                    return _resolve_refs(defs[key], defs)
                return {k: _resolve_refs(v, defs) for k, v in node.items()}
            if isinstance(node, list):
                return [_resolve_refs(v, defs) for v in node]
            return node
        
        tool_name = func.__name__
        # tool_name = f"{class_name}_{func.__name__}"
        properties = {}
        required = []
        
        for i, j in get_type_hints(func, include_extras=True).items():
            origin = j.__origin__
            if isinstance(origin, type) and issubclass(origin, BaseModel):
                schema = origin.model_json_schema()
                defs = schema.pop('$defs', {})
                if defs:
                    schema = _resolve_refs(schema, defs)
                schema["description"] = j.__metadata__[0]
                properties[i] = schema
            else:
                # 添加对 Literal 的处理
                if origin is Literal:
                    properties[i] = {
                        # "description": j.__metadata__[0] if j.__metadata__ else "",
                        "type": "string",
                        "enum": list(j.__args__)  # Literal 的值在 __args__ 中
                    }
                else:
                    properties[i] = {
                        "description": j.__metadata__[0] if j.__metadata__ else "",
                        "type": self._TYPE_MAP[origin.__name__]
                    }
        
        for i, j in inspect.signature(func).parameters.items():
            if j.default == inspect.Parameter.empty:
                required.append(i)
        
        return {
            "type": "function",
            "function": {
                "name": tool_name,
                "description": inspect.getdoc(func) or "",
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                    "additionalProperties": False
                }
            }
        }
    
    @property
    def tools(self):
        return self._tool_info


    def tool_call(self,name,args):
        # name = name.split('_', 1)[1]
        res = "没有这个工具"
        if name in self.ctools:
            res = self.ctools[name][0](**args)
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

        self._prompts = {
            "system":prompt
        }

        self._message = []
        self._work_message = []
        self._clean_index = []
        self._function_map = {
            "user":self._add_user_msg,
            "tool":self._add_tool_msg,
            "bot":self._add_bot_msg,
        }


    # def _digest_tool_msg(self):
    #     ...

    def build_message(self):
        prompt_content = ""
        for i,j in self._prompts.items():
            prompt_content+=f"[{i}] {j}"

        prompt = [{
            "role":"system",
            "content":prompt_content
        }]
        message = self._message
        work_message = self._work_message
        return prompt+message+work_message
        
    def push(self,
            msg,
            role,
            is_work=False,
            ):
        if is_work:
            self._add_work_msg(msg,role)
        else:
            if self._work_message:
                self._clear_work()
            self._function_map[role](msg)

        

    def _add_user_msg(self,msg):
        self._message.append(
            {
                "role":"user",
                "content":msg
            }
        )

    def _add_bot_msg(self,msg,x="Default"):
        if x=="Default":
            x = self._message

        x.append(msg)

    def _add_tool_msg(self,res,x="Default"):
        if x=="Default":
            x = self._message
        # if res.is_clean:

            
        x.append(
            {
            "role":"tool",
            "tool_call_id":res.tool_id,
            "content":f"工具：{res.tool_name} 输出：{res.res}"
            }
        )

# 2026/07/15 01:04:懒得取名字了，就用x来代替下吧

    def _add_work_msg(self,res,role):
        self._function_map[role](res,x=self._work_message)

        if isinstance(res,structs.TodoRes):
            self._clear_work()
            
            self._work_message.append(
                            {
                "role":"user",
                "content":res.work_prompt
            }
        )


    def edit_prompt(self):
        ...

    def _clear_work(self):
        self._work_message = []

    def clear(self):
        if self._clean_index:
            for i,j in self._clean_index:
                self._message[i]["content"] = (
                f"读取完毕，内容删除。如需读取，还请调用{j}加载"
                )
            self._clean_index = []




class Agent:
    def __init__(
            self,
            api_key,
            tools = [],
            base_url = "https://api.deepseek.com",
            modle = "deepseek-v4-flash"
        ):

        self.modle = modle
        self._messages = MessageManager()
        self._tools = tools
        self.default_tools = default_tools()
        self._mcp_client = xlmcp_client()
        self._llm = llm(api_key,base_url)
        # self.clear_tools = self.default_tools.clear_tools

    def _call_tool(self,tool_calls,is_work):

        for tool in tool_calls:
            r = structs.ToolRes()

            tool_name = tool.function.name
            tool_id = tool.id
            args = tool.function.arguments
            args = json.loads(args)
            is_clean = False


            if tool_name in self.default_tools.ctools:
                res = self.default_tools.tool_call(tool_name,args)
            else:
                res = self._mcp_client.tool_call(tool_name,args)      

            if isinstance(res,structs.Todo):
                is_work = True
                r.todo = res

            # if tool_name in self.default_tools.clear_tools:
            #     is_clean = True

            r.res = res
            r.tool_name = tool_name
            r.args = args
            r.tool_id = tool_id
            r.is_clean = is_clean

            if isinstance(res,structs.TodoRes):
                if res.done:
                    is_work = False
                vars(r).update(res.__dict__)
                
            r.is_work = is_work

            yield r

    def _loop(self,user_msg):
        tools = self.default_tools.tools+self._tools
        messages = self._messages
        is_work = False
        messages.push(user_msg,'user',is_work)

        while True:
            reply = self._llm.chat(
                tools,
                messages.build_message()
                )
            reply_msg = reply.choices[0].message
            messages.push(reply_msg,'bot',is_work)
            yield 'bot',reply

            tool_calls = reply_msg.tool_calls

            if not tool_calls:
                break

            # res,is_work_t,clean_tools_index = (
            #     yield from self._call_tool(tool_calls)
            #     )         
            gen = self._call_tool
            for i in gen(tool_calls,is_work):

                self._messages.push(
                    i,"tool",is_work
                )


                is_work = i.is_work

                yield "tool",i      

    def send(self,msg):

        for i,j in self._loop(msg):
            if i == 'bot':
                yield {
                    "type":"bot",
                    "body":{
                        "msg":j.choices[0].message.content,
                        "think":j.choices[0].message.reasoning_content
                    },
                    # "raw_data":
                }
            else:
                yield{
                    "type":"tool",
                    "body":{
                        "name":j.tool_name,
                        "args":j.args,
                        "res":j.res,
                        "time":datetime.now().strftime("%Y/%m/%d %H:%M")
                    },
                    "is_work":j.is_work,
                    "todo":j.todo,
                    # "raw_data":j
                }


        


    


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
    t = default_tools()
    ...


# 2026/07/17 21:49:基本实现todo,修复了些bug，现在就差mcp和记忆系统了




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





2026/07/14 19:27:
就是我懒了，14天都没怎么写过什么代码（
todo的思路

创建todo
提交task
启动的todo=>派出任务1
完成task=>派出下一个任务
...
完成最后一个任务=>标记todo结束






"""



