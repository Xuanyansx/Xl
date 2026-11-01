

class ToolManager:
    def __init__(self,cfg,tools_dict:dict[str,type]):
        self.cfg = cfg
        self.tools = []