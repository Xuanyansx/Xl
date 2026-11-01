from dataclasses import dataclass, field


class BaseMsgBlock:
    ...


@dataclass
class Message:
    ...

@dataclass
class Turn(BaseMsgBlock):
    ...

@dataclass
class Work(BaseMsgBlock):
    ...