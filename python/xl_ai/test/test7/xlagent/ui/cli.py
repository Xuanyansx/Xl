import prompt_toolkit
from xlagent.structs import events


class CliRun:
    def __init__(self):
        pass

    def chat(self):
        while True:
            user_msg = prompt_toolkit.prompt("[Xl_AI]< ")
            event = yield user_msg
            print(event)
