# 混合客户端，之后打算将这个改成混合客户端，但是那就是后面的事了 2026/06/28 20:28
# ps:混合客户端就是集成链接所有配置文件的服务，然后在写两个工具了，搜索工具和工具执行的工具，这样就不必暴露所有的工具了，当然这就是后话了 2026/06/28 20:30

import mcp

class xlmcp_client:
    def __init__(self):

        pass

    @property
    def tools(self):
        ...

    def tool_call(self,name,args):
        ...

    @property
    def failed_tools():
        ... 