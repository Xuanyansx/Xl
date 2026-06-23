from pathlib import Path

mcp_config = {
    "mcpServers": {
        "default": {
            "command": "python",
            "args": [str(Path(__file__).parent / "default_tools.py")]
        },  
        "burpsuite": {
            "command": "java",
            "args": [
                "-jar",
                "/home/xuanyansx/Desktop/mcp/mcp-proxy.jar",
                "--sse-url",
                "http://127.0.0.1:9876"
            ],
            "keep_alive": False
        },
        "bilibili-search": {
            "command": "npx",
            "args": ["bilibili-mcp-js"],
            "description": "B站视频搜索 MCP 服务，可以在AI应用中搜索B站视频内容。",
            "keep_alive": False

        },
        "bing-search": {
            "command": "npx",
            "args": [
                "-y",
                "bing-cn-mcp"
            ],
            "keep_alive": False
        },
        # "servers": {
        #     "cve-intelligence": {
        #     "type": "stdio",
        #     "command": "npx", 
        #     "args": ["-y", "mcp-cve-intelligence-server-lite@latest"],
        #     "keep_alive":False
        #     }
        # }

    }
}