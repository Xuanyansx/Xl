# from typing import Dict
from pydantic import BaseModel, Field
from dataclasses import dataclass, field


class DebugMixin:
    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

class BaseMsgBlock:
    def __init__(self):
        self.insert_index = []
        self.insert_msg = []

        self._normal_msg = []
        self._last_index = 0
        self._cursor = 0

    def push(self,msg,flag=False):
        if flag:
            if not self._cursor:
                self._cursor = len(self._normal_msg)
            self._append_insert(self._cursor,msg)
        else:
            self._normal_msg.append(msg)
        self._cursor+=1   
            
    def _append_insert(self, i, v):
        v = [v]
        if i - self._last_index == 1:
            self.insert_msg[-1] += v
        else:
            self.insert_index.append(i)
            self.insert_msg.append(v)
            self.last_index = i

    @property
    def message(self):
        res = self._normal_msg.copy()
        for i,j in enumerate(self.insert_index):
            res[j:j] = self.insert_msg[i]

        return res

@dataclass
class PromptClass:
    prompt: str = None 




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
    tasks:list = field(default_factory=list)
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



@dataclass
class ToolRes(DebugMixin):
    i: int
    n: int
    tool_name: str = None
    args: object = None
    tool_id: str = None
    prompt:str = None
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
        if isinstance(value,PromptClass):
            self.prompt = value.prompt
        self._res = value

        if isinstance(value,TodoRes):
            self.work_enable = value.work_enable

    # is_clean:  = None
    # is_work: object = None

@dataclass
class TodoRes(DebugMixin,PromptClass):
    res: str = None
    work_enable: bool = None
    todo: Todo = None


@dataclass
class Message:
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
    index: int = 0

    def __post_init__(self):
        super().__init__()
    ...



@dataclass
class Turn(DebugMixin,BaseMsgBlock):
    user_msg: str

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
        self._work = Work()

    def work_push(self,msg,flag=False):
        if not self._work.index:
            self._work.index = self._cursor

        self._work.push(msg,flag)

    @property
    def message(self):
        res = super().message
        wi = self._work.index
        res[wi:wi] = self._work.message
        return [self.user_msg]+res





    

             

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
