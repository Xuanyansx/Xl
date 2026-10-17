
from dataclasses import dataclass, field


@dataclass
class ReadReturn:
    mode:str
    content:str = ""
    err_text:str = ""
    end_text:str = ""

class GrepReturn:
    stderr:str
    stdout:str
    