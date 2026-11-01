from .cli import CliRun
from .web import WebRun
from xlagent.core.config import Config


class User:
    def __init__(self,ui_type:int):
        self.ui_type = ui_type
        self.ui_list = CliRun,WebRun

    def chat(self):
        user = self.ui_list[self.ui_type]()
        func = user.chat()
        msg = next(func)

        while True:
            event = yield msg 
            msg = func.send(event)
        #  2026/11/01 16:42: 脑袋要烧掉啦~
                

            


