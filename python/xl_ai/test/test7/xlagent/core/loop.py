from typing import TYPE_CHECKING
from xlagent.structs import events
from xlagent.structs import models

if TYPE_CHECKING:
    from xlagent.types import AgentConfig, ContextManager, LLMClient, ToolManager

class Agent:
    def __init__(
        self,
        cfg: AgentConfig,
        ctx: ContextManager,
        tool: ToolManager,
        llm: LLMClient,
    ):
        self.cfg = cfg
        self.ctx = ctx
        self.tool = tool
        self.llm = llm
        
    def ask(self,msg:str):

        self.ctx.push(msg)
        while True:
            reply = self.llm.chat(
                self.tool.tools,
                self.ctx.messages
            )
            return reply