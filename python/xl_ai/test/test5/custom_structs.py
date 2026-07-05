from typing import Dict
from dataclasses import dataclass, field

@dataclass
class Task:
    id:str        
    description:str
    # priority:int    
    todo_id:str
    status:str = "pending"    #pending/in_progress/done/failed


@dataclass
class Todo:
    id:str
    title:str
    description:str
    time:str
    tasks:Dict[str,Task] = field(default_factory=dict)
    _last_id = field(default=0, init=False)

    def add_task(self,Task):
        self._last_id+=1
        task_id=self._last_id
        self.tasks[task_id] = Task


