from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from xlagent.types import CTXConfig

class ContextManager:
    def __init__(
            self,
            cfg:CTXConfig
        ):
        self.cfg = cfg
        self._messages = []

    def push(self,msg):
        self._messages.append(
            {
                "role":"user",
                "content":f"message:{msg}"
            }
        )

    @property
    def messages(self):
        return self._messages
    

