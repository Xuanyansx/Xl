from fastmcp import Client
import asyncio
from pathlib import Path

async def main():
    # 方式一：使用配置字典（多服务端模式）
    config = {
        "mcpServers": {
            "default": {
                "command": "python",
                "args": [str(Path(__file__).parent / "default_tools.py")]
            },
            "burpsuite": {
                "transport": "sse",
                "url": "http://127.0.0.1:9876"
            },
            "bilibili-search": {
                "command": "npx",
                "args": ["bilibili-mcp-js"],
                "description": "B站视频搜索 MCP 服务，可以在AI应用中搜索B站视频内容。"
            },
            "bing-search": {
                "command": "npx",
                "args": [
                    "-y",
                    "bing-cn-mcp"
                ]
            }
        }
    }
    client = Client(config)
    async with client:
        tools = await client.list_tools()
        print(tools)
        for tool in tools:
            print(f"工具名: {tool.name}")
            print(f"描述: {tool.description}")
            print("-" * 50)

        ress = await client.call_tool("bing-search_bing_search",{"query":"gw"})
        print(ress)

asyncio.run(main())