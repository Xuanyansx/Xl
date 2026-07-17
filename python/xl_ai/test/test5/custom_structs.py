from typing import Dict
from pydantic import BaseModel, Field
from dataclasses import dataclass, field


class DebugMixin:
    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"


@dataclass
class Task:
    id:str        
    description:str
    content:str
    # priority:int    
    todo_id:str
    status:str = "pending"    #pending/done/failed



@dataclass
class Todo:
    id:str
    ttitle:str
    description:str
    time:str
    tasks:Dict[str,Task] = field(default_factory=dict)
    status:str = "undone"    #undone/done

    task_result = []
    running_task_id:int = field(default=0, init=False)
    _last_id:int = field(default=0, init=False)

    def add_task(self,task_des,content):
        task_id=self._last_id
        task = Task(task_id,task_des,content,self.id)
        self.tasks[task_id] = task
        self._last_id+=1


class ToolRes(DebugMixin):
    def __init__(self):
        self.res = None
        self.work_prompt = None
        self.todo = None
        self.done = None
        self.tool_name = None
        self.args = None
        self.tool_id = None
        self.is_clean = None
        self.is_work = None

class TodoRes(DebugMixin):
    def __init__(self):
        self.res = None
        self.work_prompt = None
        self.done = None
        self.todo = None


class TaskItem(BaseModel):
    description: str = Field(description="任务主题和目标")
    content:str = Field(description="任务描述")
class ttttt(BaseModel):# 2026/07/05 18:55:   懒得取名字了（（（希望以后的我看见不要吐槽
    todos: list[TaskItem] = Field(description="完整的 todo 列表，按执行顺序排列")
    model_config = {"extra": "forbid"}

