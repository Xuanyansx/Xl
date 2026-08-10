import json
import asyncio
import inspect
from openai import OpenAI
from datetime import datetime
from pydantic import BaseModel
import custom_structs as st
from xl_mcp.mcp_cs import xlmcp_client
from prompt_toolkit import PromptSession
from typing import Annotated,Literal,get_type_hints




class LLM:
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
        self.todos = []


    def create_todo(
            self,
            title:Annotated[str,"todo标题"],
            description:Annotated[str,"描述"]
        ):
        """
        create_todo 工具说明：
        - 你必须要先对目标进行评估测试，然后再创建todo和规划任务
        - 然后使用add_task依次往里面添加任务列表
        - 适用场景举例：
        a) 明确的多步骤任务（如"先A再B然后C"）
        b) 探索性研究任务（可以先规划探索方向/测试用例分组）
        c) 需要在多个工具间切换协作的任务
        - 注意：即使任务是探索性的、结果不确定的，也建议先创建todo来规划大致的步骤框架
        
        """
        todo_id = len(self.todos)
        ctime = datetime.now().strftime("%Y/%m/%d %H:%M")
        self.todos.append(
            st.Todo(
                todo_id,
                title,
                description,
                ctime
            )
        )
        return f"ok todo id : {todo_id}"

    def add_task(
            self,
            title:Annotated[str,"任务d题和目标"],
            content:Annotated[str,"任务描述"],
            todo_id:Annotated[int,"目标todo的id"]
            
        ):
        """
        请按顺序添加任务，任务派遣顺序为先进先出
        任务列表最少存在2个任务
        
        """

        if len(self.todos)<=todo_id:
            raise st.TodoError(
                f"没有这个todo，当前todos{[
                    (i.id,i.ttitle,i.status) 
                    for i in self.todos
                ]}"
            )
        
        todo = self.todos[todo_id]
        if todo.status in ["done","runing"]:
            raise st.TodoError(
                f"这个todo已经{todo.status} 无法添加"
            )

        tasks = todo.add_task(
            title,
            content
        )
        return f"ok {tasks}"

    def start_todo(
            self,
            todo_id:Annotated[int,"指定的todo的id"]
       ):
        """
        开始完成指定todo的任务，在此之前你必须添加任务
        """

        if len(self.todos)<=todo_id:
            raise st.TodoError(
                f"没有这个todo，当前todos{[
                    (i.id,i.ttitle,i.status) 
                    for i in self.todos
                ]}"
            )

        todo = self.todos[todo_id]
        tasks = todo.tasks

        if todo.status in ["done","runing"]:
            raise st.TodoError(
                f"这个todo已经{todo.status},请反思为什么要继续运行这个todo"
            )
        
        if len(todo.tasks)<2:
            raise st.TodoError(
                f"任务列表任务太少，请添加任务 当前任务列表{[
                    (i.ttitle)
                    for i in todo.tasks
                ]}"
            )
        todo.status = "runing"
        
        prompt = f"""
            当前任务: 任务id{tasks[0].id} 任务主题{tasks[0].ttitle}
            任务描述：{tasks[0].content}

            下一个任务: 
                任务id{tasks[1].id} 任务主题{tasks[1].ttitle}

            """
        res = st.TodoRes(
            prompt,
            "ok",
            True,
            todo
        )
        return res
        

        

    def update_task_status(
            self,
            todo_id:Annotated[int,"todo的id"],
            status:Literal['done','failed'],
            task_notes:Annotated[str,"本次任务产生的结论，和关键的数据"]
        ):
        """
        更新当前任务的状态，调用这个工具代表当前任务已经成功或是失败了
        更新完成后如果还有任务程序会自动给你委派新的任务
        """
        
        if len(self.todos)<=todo_id:
            raise st.TodoError(
                f"没有这个todo，当前todos{[
                    (i.id,i.ttitle,i.status) 
                    for i in self.todos
                ]}"
            )

        todo = self.todos[todo_id]
        tasks = todo.tasks
        running_task_id = todo.running_id
        next_task_id = todo.next_id

        tasks[running_task_id].status = status
        todo.task_notes.append(task_notes)

        work_enable = None
        if next_task_id == -1:
            prompt=f"""
            你完成了这个todo，
            请报告todo完成的情况

            ===
            任务产生的关键结论和数据：
            {todo.task_notes}

            ===
            """
            for i in tasks:
                prompt+=f"""
                任务完成情况
                {i.ttitle}:{i.status}
                """
            todo.status = "done"
            work_enable = False

        else:
            next_task_p = "无"
            if next_task_id+1<len(tasks):
                next_task_p = f"任务id {next_task_id+1} 任务主题 {tasks[next_task_id+1].ttitle}"
            prompt = f"""
            任务{tasks[running_task_id].id} {tasks[running_task_id].status}
        
            之前任务产生的关键数据和结论：
            {todo.task_notes}
            ====
            现在你需要完成
                任务id{next_task_id}
                任务主题{tasks[next_task_id].ttitle}
                任务描述{tasks[next_task_id].content}

            
            下一个任务：
                {next_task_p}

            """
        todo.running_id = next_task_id
        res = st.TodoRes(
            prompt=prompt,
            res="ok",
            work_enable=work_enable,
            todo=todo
        )
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
        使用系统的shell执行命令，
        底层实现是subprocess.run，
        不要执行会阻塞程序的命令
        """
        import subprocess
        res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=True
            )
        return {"stderr":res.stderr,"stdout":res.stdout,"returncode":res.returncode}




class DefaultTools:
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
            max_token,
            max_active_turn,
            max_turn,
            gc_turn,
            prompt="default",
            soul = ""
            
        ):

        if prompt == "default":
            self._prompt = "你需要装作一个真实的人类，但你不必刻意扮演其他人，请做好记忆中的自己就好了"
        self._soul = soul

        self._turns = []
        self._sub_prompts = []
        self._turn = None
        self._messages = []
        # self._cache_messages = []

        # self._turn = []

        self.max_token = max_token
        self.max_active_turn = max_active_turn
        self.max_turn = max_turn

        self._work_enable = None

        self._func_menu = {
            "user":self._add_user_msg,
            "assistant":self._add_bot_msg,
            "tool":self._add_tool_msg
        }
        
    def build_messages(self):
        prompt = [{
            "role":"system",
            "content":f"""
            {self._prompt}
            [灵魂&人格自述]
            {self._soul}

            """
        }]
        return self._messages+prompt+self._turn.message



    def push(self,message:st.Message):
        # 关于有些地方注释属性和有些地方没有注释，其实这是为了方便我补全，并不是规范（（（汗 2026/07/30 17:51:
  
        msg = message.message 
        role = message.role
        # prompt = message.prompt

        if message.work_enable != None:
            self._work_enable = message.work_enable

        msg = self._func_menu[role](role,msg)
        if role == "user":
            if self._turn:
                self.gc()

            self._turn = st.Turn(msg)
            self._turns.append(self._turn)
        else:
            for m,f in msg:
                if self._work_enable:
                    self._turn.work_push(m,f)
                else:
                    self._turn.push(m,f)


        
        
        

    # def _build_turn(self):
    #     ...

    def _add_user_msg(self,role,msg):
        return {"role":role,"content":msg}

    def _add_bot_msg(self,role,msg):
        return [(msg,False)]

    def _add_tool_msg(self,role,msg:st.ToolRes):
        res = [
                (
                    {
                    "role":role,
                    "tool_call_id":msg.tool_id,
                    "content":f"{msg.res}"
                    },
                    msg.is_clear
                )
            ]
        if msg.prompt:
            self._sub_prompts.append(
                (
                    {
                        "role":"user",
                        "content":msg.prompt,
                        "name":"[系统]"
                    },
                    False
                )
            )
        if msg.is_last:
            res+=self._sub_prompts
            self._sub_prompts = []


        return res

            

    # def _add_work_msg(self,role,msg):
    #     return [()]
    #     ...

    
    def gc(self):
        self._messages+=self._turn.message



class Agent:
    def __init__(
            self,
            api_key,
            base_url,
            modle,
            max_token,
            max_active_turn,
            max_turn,
            gc_turn,
            tools
            # tools = [],

        ):

        self.modle = modle
        self._messages = MessageManager(
            max_token,
            max_active_turn,
            max_turn,
            gc_turn
        )

        self.soul = ""
        self.skill = []
        self.tools = tools
        self.default_tools = DefaultTools()
        self._mcp_client = xlmcp_client()
        self._llm = LLM(api_key,base_url)
        # self.clear_tools = self.default_tools.clear_tools

    def _call_tool(self,tool_calls):
        n = len(tool_calls)-1
        for i,tool in enumerate(tool_calls):
            tool_res = st.ToolRes(i=i,n=n)
            name = tool.function.name
            id = tool.id
            args = tool.function.arguments
            args = json.loads(args)

            try:
                if name in self.default_tools.ctools:
                    res = self.default_tools.tool_call(name,args)
                else:
                    res = self._mcp_client.tool_call(name,args)      
            except Exception as e:
                res = f"{e}"
            
            tool_res.res = res
            tool_res.tool_id = id
            tool_res.tool_name = name
            tool_res.args = args
            tool_res.is_clear = (
                name in self.default_tools.clear_tools
                )

            yield tool_res

    def _loop(self,user_msg):
        tools = self.default_tools.tools+self.tools

        self._messages.push(
            st.Message(
                user_msg
            )
        )

        while True:
            reply = self._llm.chat(
                tools,
                self._messages.build_messages()
            )
            reply_content = reply.choices[0].message
            self._messages.push(
                st.Message(
                    reply_content,
                    "assistant"
                )
            )
            yield "bot",reply
            tool_calls = reply_content.tool_calls

            if not tool_calls:
                break

            gen = self._call_tool(tool_calls)
            for i in gen:
                self._messages.push(
                    st.Message(
                        i,
                        "tool"
                    )
                )
                yield "tool",i
        # 这解耦合不就成了吗  2026/08/02 14:58:



        
    def send(self,msg):

        for i,j in self._loop(msg):
            if i == 'bot':
                yield {
                    "type":"bot",
                    "body":{
                        "msg":j.choices[0].message.content,
                        "think":j.choices[0].message.reasoning_content
                    },
                    # "raw_data":j
                }
            else:
                # j = st.ToolRes
                todo = None
                if isinstance(j.res,st.TodoRes) and j.res.todo:
                    todo = j.res.todo
                yield{
                    "type":"tool",
                    "body":{
                        "name":j.tool_name,
                        "args":j.args,
                        "res":j.res,
                        "time":datetime.now().strftime("%Y/%m/%d %H:%M")
                    },
                    "prompt":j.prompt,
                    "is_work":j.work_enable,
                    "todo":todo,
                    "raw_data":j
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
    # t = DefaultTools()
    # t = Todo()
    # try:
    #     t.create_todo(
    #         "test",
    #         "testestwets"
    #     )
    #     t.add_task(
    #         "1111",
    #         "1111ee1",
    #         0
    #     )
    #     t.start_todo(0)
    # except Exception as e:
    #     print(f"{e}")
    print("debug")
    ...



# 草了屏幕太小了，分三屏看着好挤  2026/08/02 17:42:

# 2026/08/02 23:43:
# 我印象最深的还是test4, 
# 这是陪伴我最长时间的智能体了，
# 也是代码写的最投入的智能体了
# 最近和其他ai讨论我的项目时，时长习惯将版本好输入为test4
# 或许我的确是想她了..。或者说是想念哪个激情四射的我了，现在我写几步就会有点瓶颈，不能那愉快的流程的codeing了



"""
turn_list
[[
    *user[{"role":"user","content":xxx}]
    work[   {
            "role":assistant,
            "content":xxx
        },
        {
            "role":Tool,
            ....
        }
        ...
    ]
    *bot&tool[
    {}
    {}
    ...
    ]

]]

msg = turn_list+prompt+turn




"""

"""

"""

