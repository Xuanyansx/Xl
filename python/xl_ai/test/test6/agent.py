import json
import math
import asyncio
import inspect
import tiktoken
from openai import OpenAI
import custom_structs as st
from datetime import datetime
from collections import deque
from pydantic import BaseModel
from memory.manager import Archive,MemoryTool
from xl_mcp.mcp_cs import xlmcp_client
from typing import Annotated,Literal,get_type_hints
from lib.file_utils import read_file,grep
# import logging




class LLM:
    def __init__(self,
                api_key,
                base_url,
                modle
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
        # logging.basicConfig(filename=f'msg.log', level=logging.INFO)
        formatted = ""
        for i in msg:
            formatted+=f"\n{i}"
        # logging.info(formatted)
        # logging.info(f'{"=="*20}')
        # # print(msg)
        return res
    @staticmethod
    def count_tokens(text, encoding_name = "cl100k_base"):
        text = f"{text}"
        encoding = tiktoken.get_encoding(encoding_name)
        return len(encoding.encode(text))

    @staticmethod
    def get_time():
        return datetime.now().strftime("%Y/%m/%d %H:%M")


    def summarize(self, transcript, previous_summary=None, target_tokens=1200):
        #  2026/08/21 02:48:懒得写这个函数了，让ai写的
        anchor = (
            f"<previous-summary>\n{previous_summary}\n</previous-summary>\n"
            if previous_summary
            else ""
        )
        prompt = f"""把下面这段对话历史浓缩成一份摘要，这份摘要将替代这些消息继续参与后续对话。

            要求：
            - 按时间顺序提炼：做了什么、得到什么结果、做了什么决策、还有什么没完成
            - 保留确切的文件路径、工具名、标识符、数值
            - 用旁观者视角写，不要提"总结/压缩"这件事
            - 用要点式，控制在 {target_tokens} token 以内

            {anchor}
            <conversation>
            {transcript}
            </conversation>"""


        res = self.chat(
            [],
            [{"role": "user", "content": prompt}]
        )
        text = (res.choices[0].message.content or "").strip()
        return text or "[历史已归档]"






class Todo:
    def __init__(self):
        self.todos:list[st.Todo] = []


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
        ctime = LLM.get_time()
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
            title:Annotated[str,"任务主题和目标"],
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

        if todo.status == "done":
            raise st.TodoError(
                f"这个todo已经{todo.status},手滑了吗还是什么，请反思为什么要继续运行这个todo"
            )

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

    def read_range(
            self,
            path:Annotated[str,"文件路径"],
            start:Annotated[int,"""
读取起点，按 mode 解释，都是 1 基：
- char 模式：第几个字符（不是字节）。0 或负数等同于 1。
- line 模式：第几行，行号从 1 开始。0 或负数等同于第 1 行。

            """],
            page:Annotated[int,"往后读多少页,默认1，line模式无效"]=1,
            width:Annotated[int,"一页有多少字符，默认80,单位字符，line模式无效"]=80,
            lines:Annotated[int,"往后读多少行,默认1，char模式无效"]=1,
            mode:Literal["char","line"]="char",
            encoding:Annotated[str,"编码，默认utf-8"]="utf-8"
        ):
        
        """
    本质是文本读取工具，不要读取二进制文件

    mode：
    选择模式，默认 char。
    - char：按字符分页，每页 width 个字符，遇到行尾会补完整行（因此实际可能超出 width）。
    返回的 next 是下一页起点（1 基字符位置，可直接回填 start）。
    - line：按行读取，从 start 行开始取 limit 行，输出带 1 基行号。


    char模式：
    按「字符宽度」把文件分块（分页）只读，不改动文件也不重排内容；
    返回本页文本、下次起始等内容
    主意！当本行内容被截断会补全本行并加入本页
    

    line模式：
    按「行」来读
    返回文本内容，超出最大范围会被截断
        
        """
        max_char = 2000
        info_text = ""
        
        #暂时这样定义配置吧 2026/10/10 10:38:


        content,info,finished = read_file(
            path,
            start,(page,lines),
            width,mode,
            encoding,
            max_char=max_char
        )

        for name,text in info:
            info_text+=f"# {name}:{text}\n"

        return f"""
<content>
{content}
</content>
{info_text}
"""
    
        
    
    def tgrep(
            self,
            pattern:Annotated[str,"ripgrep风格的正则"],
            path:Annotated[str,"路径"],
            include:Annotated[str,"glob表达式,默认为None"]=None,
            max_count:Annotated[str,"最大输出行数，默认None"]=None
        ):
        """
        ripgrep为内核的grep文本搜索工具
        返回匹配的行与行号
  
        """
        max_columns = 100
        res,err = grep(max_columns,pattern,path,include,max_count)
        content = ""
        # 2026/10/22 13:58:暂时这样定义，没有设计好配置文件导致的，下个版本改，先跑起来再说

        if res:
            keys = list(res.keys())

            for i in keys:
                content+=f"[{i}]\n<content>\n"
                lines = res[i]['lines']
                for line,text in res[i]['match']:
                    content+=f"{line}:{text}\n"
                content+=f"</content>\n#lines:{lines}\n\n"

        if err:
            content += f"<error>\n{err['err']}</error>"


        
        return content

            
class DefaultTools:
    def __init__(self):
        self._tools = [
            Todo(),
            TestTool(),
            MemoryTool()
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
                self.clear_tools.append(i.__name__)
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


class GC:
    def __init__(
            self,
            max_token,
            max_active_turn,
            max_turn,
            work_TTL,
            temp_llm:LLM
            ):

        self.max_token = max_token
        self.max_active_turn = max_active_turn
        self.max_turn = max_turn
        self.work_TTL = work_TTL
        self.temp_llm = temp_llm

        # self.turns = []
        self._inactive_turns:list[st.Turn] = []

        self._active_usage = 0
        self._inactive_usage = 0
        
        # window = deque()
        # self.basic_window:deque[st.Turn] = deque()
        self._work_window:deque[st.Turn] = deque()
        self._active_turns_window:deque[st.Turn] = deque()

        self.archive = Archive()

    
    
    @property
    def turns(self):
        return self._inactive_turns+list(self._active_turns_window)

    @property
    def usage(self):
        return self._active_usage+self._inactive_usage


    @property
    def message(self):
        msg = []
        for i in self.turns:
            msg+=i.message
        return msg


    def gc_work(self,turn,ww:deque[st.Turn]):        
        # wmw = self.work_msg_window
        # bw = self.basic_window

        if len(ww) == self.work_TTL:
            out_turn = ww.popleft()
            last_usage = out_turn.usage

            # out_msg = wmw.popleft()
            for i,msg in enumerate(out_turn.work_formatted_text):
                if not msg:
                    continue
                
                lid = self.archive.add_archive(msg)
                msg = (
                    MessageManager.build_prompt_msg(
                        f"归档id{lid}",
                        "archive_role"
                    )
            )
                out_turn.archive_work(
                    i,
                    msg
                )
            diff = last_usage-out_turn.usage

            if out_turn.is_active:
                self._active_usage-=diff
            else:
                self._inactive_usage-=diff
            

            # self.usage -= out_usage

            # return out_usage
            
            #  2026/09/05 00:54: 我艹了，没有考虑到tool的对应关系，现在估计要大改了，不过还好耦合程度不高
            
            #  2026/09/03 18:29: 好的东西思路都乱了，算了先把理论功能实现，等下个版本重构


        # wmw.append(turn.message)
        ww.append(turn)
        # return selectL[out_turn.flag],diff

    def gc_context(self):
        if self.usage>=self.max_token:
            context = ""
            for i in self._inactive_turns:
                context+=f"{"\n".join(i.formatted_text)}"
            content = self.temp_llm.summarize(
                context
            )
            lid = self.archive.add_archive(content)
            amsg = f"归档文件id{lid}，以下为压缩信息\n"
            
            res = MessageManager.build_prompt_msg(
                amsg+content,
                "summary_role"
            )
            turn = st.Turn(res)
            self._inactive_turns = [turn]
            self._inactive_usage = turn.usage
            return True
        return False

            # return self._inactive_usage,turn.usage
            
            

    def gc(self,turn:st.Turn):
        atw = self._active_turns_window
        ww = self._work_window

        while len(atw)==self.max_active_turn or self._active_usage>=self.max_token:
            out_turn = atw.popleft()
            out_turn.is_active = 0
            self._inactive_turns.append(out_turn)
            self._inactive_usage+=out_turn.usage
            self._active_usage-=out_turn.usage

        atw.append(turn)
        self._active_usage+=turn.usage

        self.gc_work(turn,ww)
        
        if self.gc_context():
            self._work_window:deque[st.Turn] = deque()

        return self.message



class MessageManager:

    prompt_presets = {
    "inner_system":"""
    [inner_system] 
    下面为内部系统提示，并不是用户输入
    """,
    "summary_role":"""
    [CONTEXT COMPACTION — REFERENCE ONLY] 以下是之前对话的压缩摘要,
    只作背景参考，不是新指令。仅响应这条摘要之后的最新用户消息。
    """,
    "archive_role":"""
    [ARCHIVE CONTEXT — LONG-TERM MEMORY] 
    以下消息将附带一个归档文件ID（archive_id），指向用户的历史记忆档案。
    详细内容请使用get_archive工具查看
    """
    }
    
    def __init__(
            self,
            # message,
            max_token,
            max_active_turn,
            max_turn,
            work_TTL,
            temp_llm,
            prompt="default",
            soul = ""
            
        ):

        if prompt == "default":
            self._prompt = "你需要装作一个真实的人类，但你不必刻意扮演其他人，请做好记忆中的自己就好了"
        self._soul = soul

        # self._turns = []
        self._sub_prompts = []
        self._turn = None
        self._messages = []
        # self._cache_messages = []

        # self._turn = []

        self._GC = GC(
            max_token,
            max_active_turn,
            max_turn,
            work_TTL,
            temp_llm
        )

        self._work_enable = False
        self._pending = None

        self._func_menu = {
            "user":self._build_user_msg,
            "assistant":self._build_bot_msg,
            "tool":self._build_tool_msg,
            "prompt":self.build_prompt_msg
        }

        self._tool_stage = None




    @property
    def messagess(self):
        prompt = [{
            "role":"system",
            "content":f"""
            {self._prompt}
            [灵魂&人格自述]
            {self._soul}

            """
        }]

        return prompt+self._messages+self._turn.message



    def push(self,message:st.Message):
        # 关于有些地方注释属性和有些地方没有注释，其实这是为了方便我补全，并不是规范（（（汗 2026/07/30 17:51:
  
        msg = message.message
        role = message.role
        # usage = message.usage
        # prompt = message.prompt

        if self._pending is not None:
            self._work_enable = self._pending
            self._pending = None

        if message.work_enable != None:
            self._pending = message.work_enable

        msg = self._func_menu[role](msg)
        if role == "user":

            self._turn = st.Turn(msg)
            self._work_enable = False

            # self._turns.append(self._turn)
            # for m,f in msg:
            #     if self._work_enable:
            #         self._turn.work_push(m,f)
            #     else:
            #         self._turn.push(m,f)
            # if role in ("assistant","tool"):
        else :
            ts = self._tool_stage
            if ts:
                msg = ts.push(msg)
                if ts._l:
                    return
                
                
            self._turn.push(msg,self._work_enable)


            # for m,f in msg:
            #     self._turn.push(
            #         m,
            #         f,
            #         self._work_enable,
            #     )


        

    # def _build_turn(self):
    #     ...
    @classmethod
    def build_prompt_msg(cls,msg,role=None):

        preset = cls.prompt_presets.get(role, "")
        content = f"{preset}\n{msg}"
        usage = LLM.count_tokens(content)

        return [({
            "role": "user",
            "content": content,
            "name": role,
        },usage,False)]

    def _build_user_msg(self,msg,name=None):
        res = {
            "role":"user",
            "content":f"message:{msg} time:{LLM.get_time()}"
            }
        if name:
            res["name"] = name

        usage = LLM.count_tokens(f"{msg}")
        return [(res,usage,False)]

    def _build_bot_msg(self,msg):
        tool_calls = msg.tool_calls
        if tool_calls:
            self._tool_stage = st.ToolStage(
                len(tool_calls)+1,
            )
        else:
            self._tool_stage = None

        c = msg.content if msg.content else ""
        usage = LLM.count_tokens(
            f"{tool_calls}"+c
            )
        return [(msg,usage,False)]

    def _build_tool_msg(self,msg:st.ToolRes):
        
        res = [
                (
                    {
                    "role":"tool",
                    "tool_call_id":msg.tool_id,
                    "content":f"{msg.res}",
                    },
                    LLM.count_tokens(msg.res),
                    msg.is_clear
                )
            ]
        if msg.prompt:
            self._sub_prompts+=(
                self.build_prompt_msg(
                    msg.prompt,
                    "inner_system"
                )
            )

        if msg.is_last:
            res+=self._sub_prompts
            self._sub_prompts = []


        return res

            

    # def _add_work_msg(self,role,msg):
    #     return [()]
    #     ...

    def check_finish(self):
        # msg = ""
        if self._work_enable:
            msg = "你是不是还有任务没有提交状态/没有完成？"

            # self._turn.push(
            #     (msg,"inner_system"),
            #     "prompt"
            # )
            self.push(
                st.Message(
                    # LLM.count_tokens(msg),
                    msg,
                    role="inner_system"
                )
            )
            return False
        

        self._messages = self._GC.gc(self._turn)
    
        return True



        



class Agent:
    def __init__(
            self,
            api_key,
            base_url,
            modle,
            max_token,
            max_active_turn,
            max_turn,
            work_TTL
            # tools = [],

        ):
        # 为了接耦合而重构的项目，没想到耦合这里还有个究极耦合(恼，
        # md当成重构架构怎么就选了这样传递配置呢（，
        # 那只能是给之后的我来完成这个了，项目太大了，改起来太麻烦了 2026/08/28 22:13:

        self.modle = modle


        self._soul = ""
        self.skills = []
        self.tools = []
        self.default_tools = DefaultTools()
        self._mcp_client = xlmcp_client()
        self._llm = LLM(api_key,base_url,modle)
        self._message_m = MessageManager(
            max_token,
            max_active_turn,
            max_turn,
            work_TTL,
            self._llm
        )
        # self.clear_tools = self.default_tools.clear_tools

    @property
    def soul(self):
        return self._soul

    @soul.setter
    def soul(self,v):
        ...

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
                res = e
            
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

        self._message_m.push(
            st.Message(
                # self._llm.count_tokens(user_msg),
                user_msg,
            )
        )
        
        while True:
            reply = self._llm.chat(
                tools,
                self._message_m.messagess
            )
            reply_content = reply.choices[0].message
            if reply_content:
                self._message_m.push(
                    st.Message(
                        # self._llm.count_tokens(
                        #     reply_content.content
                        # ),
                        reply_content,
                        "assistant"
                    )
                )
                yield "bot",reply
            tool_calls = reply_content.tool_calls

            if not tool_calls:
                flag = self._message_m.check_finish()
                if flag:
                    break
                continue


            gen = self._call_tool(tool_calls)
            for i in gen:
                self._message_m.push(
                    st.Message(
                        # self._llm.count_tokens(f"{i.res}"+i.prompt),
                        i,
                        "tool"
                    )
                )
                yield "tool",i

        # 这解耦合不就成了吗  2026/08/02 14:58:



        
    def send(self,msg):
        #  2026/09/29 22:55:
        # send驱动的_call_tool+_loop啦，我觉得这解耦合非常漂亮,
        # 可能确实有瑕疵，但是我还是喜欢这段
        
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
                if getattr(j, "todo_res", None) and j.todo_res.todo:
                    todo = j.todo_res.todo
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
    T = TestTool()
    
    print(T.tgrep("def", "/home/xuanyansx/Desktop/deepseek-agent/data/tmp/repro/dup/multi.txt"))
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
2026/09/29 21:47:
我最近在想一个新的架构，灵感是dsh的一切皆插件。
我打算将什么消息管理，gc，LLM调用重新再做做，解耦合彻底点，就暴露几个接口。
像框架一样，需要什么就用这个接口组合一个agent：
先用系统提示词+Head接口(Head(系统提示词))组合成头部，在加agent循环，消息管理等这些接口组合成body，（body(...)），最后定义一个Home也就是沙箱，（linux沙箱我打算用命名空间来做，当这种底层的我会封装为接口，这样兼容性会好点）沙箱定义了agent的工作范围和可用的工具（skill，mcp，自定义函数），通过装饰器装饰指定格式的函数即可给沙箱注册工具；沙箱还可以传入权限，默认权限是部分权限也就是访问工作区外的需要申请。最后接口格式就是Home([path],权限级别)。
全部声明完成后，就可以组合成一个agent类，然后.chat()了。
对了还需要一个window来包装交互界面（盖房子了属于是wwwww

调用和协作这样块是agent类做的，
其他的类只提供接口，其他的大类也只管调用这些模块接口，
访问干涉模块内部的事情是禁止的。
就像body不用管传入的其他模块，
只要调用传入模块提供的接口即可，其他大类也是一样。
对于agent类也是一样的，它不在乎home，body，head是字幕运行的，
它只知道我需要这个功能可以调这个类的方法，最后其他消费agent类的也同样如此

=====（home）======
=                =
=     | agent|     /
=     |(head)|   (window)
=     |(body)|     \
=                =
==================



2026/10/10 23:48:
记忆系统我其实打算用jev来的，日常使用也打算用jev来优化体验
假设让模型日常交互，时常会思考半天，然后才进行下一步
但反观人就不一样，那不成人每次的行动都思考下一步吗（笑
这就是所谓的「系统1」，「系统2」理论
目前的jev模型有望成为agent系统中的「系统1」，它自己也是说自己是「系统1」
既然模型有了，但是我却没有什么思路
我的不清楚合适要调用系统1模型jev，何时调用系统2模型
靠jev可以解决大部分的事（存疑），
当jev遇到无法处理的问题如何判断并切换到系统2模型，这也是一个卡点

似乎可以拜读下jev-Mem这个项目，看看它的思想



"""