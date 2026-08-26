# 混合客户端，之后打算将这个改成混合客户端，但是那就是后面的事了 2026/06/28 20:28
# ps:混合客户端就是集成链接所有配置文件的服务，然后在写两个工具了，搜索工具和工具执行的工具，这样就不必暴露所有的工具了，当然这就是后话了 2026/06/28 20:30


from mcp.client import Client 

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


"""
2026/08/18 23:25: 
找到一篇神级教程，我的天，感觉比官方文档写的还全
所谓的绝世功法就是这样的吗，这么好的教程居然藏的如此之深
我决定了要把它学好，然后把mcp完成！这个mcp拖的太久了！
教程地址https://aiknowledge.cn/collection/1160-mcp-python-sdk-%E6%8A%80%E6%9C%AF%E6%95%99%E7%A8%8B
"""