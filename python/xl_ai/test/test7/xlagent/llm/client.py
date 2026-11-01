from xlagent.structs.options import LLM
from openai import OpenAI


class LLMClient:
    def __init__(self,cfg:LLM):
        self.cfg = cfg
        self.modle = cfg.model
        self._client = OpenAI(
            api_key=cfg.api_key,
            base_url=cfg.base_url         
        )

    def chat(self,tools,msg):
        client = self._client
        res = client.chat.completions.create(
            model=self.modle,
            tools=tools,
            messages=msg
        )
        return res      