# from typing import Dict
from itertools import pairwise
from pydantic import BaseModel, Field
from dataclasses import dataclass, field
from xl_lib import format_message



class DebugMixin:
    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

class BaseMsgBlock:
    def __init__(self):
        self._insert_index = []
        self._insert_msg = []
        self._formatted_text = ""
        self.flag = 0 # 标识被压缩
        # [[],[],[]]

        self._inner_messages = []
        self._normal_msg = []
        self._last_index = 0
        self._cursor = 0
        self.msg_changed = 0 #列表发生变化就为1  2026/08/29 01:00:
        

        
    def _push(self,message):
        for msg,flag in message:

            self._inner_messages.append(msg)
            self._formatted_text += format_message(msg)
            
            if flag:
                if not self._cursor:
                    self._cursor = len(self._normal_msg)
                self._append_insert(self._cursor,msg)
            else:
                self._normal_msg.append(msg)

            self._cursor+=1   


    def _build_message(self):
        res = self._normal_msg.copy()
        for i,j in enumerate(self._insert_index):
            res[j:j] = self._insert_msg[i]

        return res
            
    def _append_insert(self, i, v):
        # v = [v]
        if self._insert_msg and i - self._last_index == 1:
            self._insert_msg[-1] += v
        else:
            self._insert_index.append(i)
            self._insert_msg.append(v)
        self._last_index = i



    def _edit_insert_msg(self,i,msg):
        self._insert_msg[i] = [msg]
        # self.inner_messages = self._build_message()
        self.msg_changed = 1
    #  2026/08/22 23:25: 简单重构了下逻辑，这样每次获取消息就不用重新拼装了
    #  实话说我早就看这个不爽了，完成前面的任务后也是把这个不爽点修了
    
    @property
    def inner_messages(self):
        # property大法,爽！property大法,爽！!property大法,爽！! ！😋 2026/08/29 01:16:

        if self.msg_changed:
            self.msg_changed = 0
            self._inner_messages = self._build_message()
        return self._inner_messages
    # 补丁，每次edit就重构心里还是太别扭了 2026/08/29 01:05:

@dataclass
class PromptClass:
    prompt: str = ""




@dataclass
class Task:
    id:int      
    ttitle:str
    content:str
    # priority:int    
    todo_id:int
    status:str = "pending"    #pending/done/failed



@dataclass
class Todo:
    id:int
    ttitle:str
    description:str
    create_time:str
    tasks:list[Task] = field(default_factory=list)
    status:str = "undone"    #undone/runing/done
    time:str = "now" #之后或许会做定时/延迟任务

    task_notes: list = field(default_factory=list)
    running_id:int = field(default=0, init=False)


    @property
    def next_id(self):
        if self.running_id+1 == len(self.tasks):
            return -1
        return self.running_id+1


    def add_task(self,title,content):
        self.tasks.append(
            Task(
                len(self.tasks),
                title,
                content,
                self.id
            )
        )

        return self.tasks


# @dataclass
# class AssistantRes:
#     res: object
#     tool_calls: list = None


@dataclass
class ToolRes(DebugMixin):
    i: int
    n: int
    tool_name: str = None
    args: object = None
    tool_id: str = None
    prompt:str = ""
    work_enable:object = None
    is_last: bool = False
    is_clear: bool = False
    _res: object = None

    def __post_init__(self):
        if self.i == self.n:
            self.is_last = True

    
    @property
    def res(self):
        return self._res

    @res.setter
    def res(self,value):
        r = value
        if isinstance(value,PromptClass):
            self.prompt = value.prompt

        if isinstance(value,TodoRes):
            self.work_enable = value.work_enable
            r = value.res
        self._res = r
            
    # is_clean:  = None
    # is_work: object = None

@dataclass
class TodoRes(DebugMixin,PromptClass):
    res: str = None
    work_enable: bool = None
    todo: Todo = None


@dataclass
class ToolStage:
    _l: int
    item:list = field(default_factory=list)

    def push(self,msg):
        self.item+=msg
        self._l-=1
        return self.item

@dataclass
class Message:
    usage:int
    message: object
    role: str = "user"
    prompt: object = None
    work_enable:object = None

    def __post_init__(self):
        if isinstance(self.message,ToolRes):
            self.work_enable = self.message.work_enable
            self.prompt = self.message.prompt



@dataclass
class Work(BaseMsgBlock):
    i : int = 0
    index: int = 0

    @property
    def formatted_text(self):
        if self.archive_msg:
            return 
        return self._formatted_text

    def __post_init__(self):
        super().__init__()
        self.archive_msg = []

    @property
    def inner_messages(self):
        if self.archive_msg:
            return self.archive_msg
        return super().inner_messages

    



@dataclass
class Turn(DebugMixin,BaseMsgBlock):
    user_msg: str
    _work = None
    _usage: int = 0

    # a = [1,2,3,4,5,9,10,20,24,26,28,30]
    # b = [5,10,20,24,26,28]
    # c = [
    #         [6,7,8],
    #         [11,12,13,14,15,16,17,18,19],
    #         [21,22,23],
    #         [25],
    #         [27],
    #         [29]
    #     ]
    
    def __post_init__(self):
        super().__init__()
        self.works : list[Work]= []
        self._work_summarized_text: list = []
        self._formatted_text += format_message(self.user_msg)

    def archive_work(self,id,msg):
        self.works[id].archive_msg = [msg]

    @property
    def usage(self):
        return self._usage

    @usage.setter
    def usage(self,v):
        self._usage+=v

    #  2026/08/26 11:17:  艹了，设计上没有考虑多work，现在好了（


    # def push(self,msg,flag=False,work_enable=False):

    #     if work_enable:
    #         if self._work == None:
    #             self._work = Work()
    #         self._work_push(msg,flag)
    #         return

        
    #     if self._work:
    #         self.works.append(self._work)
    #         self._work = None
    #     self._push(msg,flag)
        
    def push(self,msg,work_enable=False):
        if work_enable:
            if self._work == None:
                self._work = Work()
            self._work_push(msg)
            return

        
        if self._work:
            self.works.append(self._work)
            self._work = None
        self._push(msg)



            
    def _work_push(self,msg):
        if not self._work.index:
            self._work.index = self._cursor

        self._work._push(msg)

    @property
    def work_formatted_text(self):
        return [w.formatted_text for w in self.works if w.formatted_text]
        
    @property
    def formatted_text(self):
        ...

    @property
    def message(self):
        res = self.inner_messages.copy()
        if self._work:

            wi = self._work.index
            res[wi:wi] = self._work.inner_messages

        for i in reversed(self.works):
            wi = i.index
            res[wi:wi] = i.inner_messages

        return [self.user_msg]+res


        # [0,1,2,3,4,5,6,7]
        # [1,2,3,4,5] 4:4
        # [1,2,3,4] 6:6
        # [0,1,2,3,+1,2,3,4,5+,4,5,6,7]


    @property
    def insert_messages(self):
        res = []
        for i in self.works+([self._work] if self._work else []):
            res+=i._insert_msg
        return self._insert_msg+res


    def edit_insert_msg(self, i, msg):
        l = 0
        L = [self]+self.works+([self._work] if self._work else [])
        # if i < L:
        #     self._edit_insert_msg(i,msg)
        #     return
        
        for wi,w in enumerate(L):

            if i<l+len(w._insert_msg):
                L[wi]._edit_insert_msg(
                    i-l,
                    msg
                )
                return
            l+=len(w._insert_msg)

        #  2026/08/27 01:10: 写这个edit类似我了（aidebug真好用，嘿嘿），
        # 不过好在现在彻底完成了多work的兼容了


            




        
    #     if i >= len(self._insert_msg):
    #         self.work._edit_insert_msg(
    #             i-len(self._insert_msg),
    #             msg
    #         )
    #         return

    #     self._edit_insert_msg(i,msg)

        # [0,1,2,3,4,5,6][0,1,2, 3, 4]
        # [0,1,2,3,4,5,6, 7,8,9,10,11]









    

             

class TodoError(Exception):
    pass

# class TaskItem(BaseModel):
#     description: str = Field(description="任务主题和目标")
#     content:str = Field(description="任务描述")

# class ttttt(BaseModel):# 2026/07/05 18:55:   懒得取名字了（（（希望以后的我看见不要吐槽
#     todos: list[TaskItem] = Field(description="完整的 todo 列表，按执行顺序排列")
#     model_config = {"extra": "forbid"}



if __name__ == "__main__":
    print("debug")

    # t = Turn("111")
    # while True:
    #     t.push("1111")
    #     t.push("1111")
    #     t.push("1111",True)
    #     t.push("1111")
    #     t.push("1111",True)
    #     t.push("1111",True)
    #     t.push("1111")
    #     t.push("1111")
    #     t.push("1111",True)
    #     t.push("1111",True)
    #     t.push("1111",True)
    #     t.push("1111",True)
    #     t.push("1111",True)


