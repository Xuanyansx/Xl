from dataclasses import dataclass, field



@dataclass
class LLM:
    api_key:str
    base_url:str
    model:str

@dataclass
class CTX:
    ...

@dataclass
class Tool:
    ...

@dataclass
class Agent:
    ...