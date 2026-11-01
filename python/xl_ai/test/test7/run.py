import sys
from pathlib import Path
from xlagent.default_tool import Tools
from xlagent.core.context import ContextManager
from xlagent.core.loop import Agent
from xlagent.core.tool import ToolManager
from xlagent.llm.client import LLMClient
from xlagent.core.config import Config
from xlagent.ui import User



def build_agent(cfg:Config):

    llm = LLMClient(cfg.llm)
    tools_dict = Tools.tools_dict

    ctx = ContextManager(cfg.ctx)
    tm = ToolManager(cfg.tool,tools_dict)

    return Agent(cfg.agent,ctx,tm,llm)

def select_ui():
    ui = ['cli','web']
    sel = sys.argv
    if len(sel)>1:
        if sel[1] not in ui:
            print("没有这个启动方式，可以试试web或者cli")
            return None
        sel = 1
    else:
        sel = 0

    return User(sel)

def main():

    parent_path = Path(__file__).resolve().parent
    cfg_path = parent_path / "data" / "config" / "config.json" 
    cfg = Config(cfg_path)

    user = select_ui()
    if not user:
        return
    func = user.chat()
    user_msg = next(func)

    agent = build_agent(cfg)

    while True:
        event = agent.ask(user_msg)
        user_msg = func.send(event)


if __name__ == "__main__":
    main()