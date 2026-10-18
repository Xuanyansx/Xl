
from dataclasses import dataclass, field


@dataclass
class ReadReturn:
    mode:str
    content:str = ""
    err_text:str = ""
    end_text:str = ""

@dataclass
class GrepReturn:
    content:list
    err_text:list = field(default_factory=list)
    