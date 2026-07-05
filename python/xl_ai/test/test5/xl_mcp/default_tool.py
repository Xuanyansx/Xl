class Task:
    id: str        
    description: str
    status: str   #pending/in_progress/done/failed
    priority: int    
    todo_id: str


class todo:
    title:str
    description:str
    tasks:list[Task]
    time:str