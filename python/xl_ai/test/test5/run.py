import agent
import xl_mcp.mcp_cs
import prompt_toolkit
import xl_config.config as c
# import xl_config.mcp_config as 



def main():
    Config = c.Config
    config = Config
    key = Config["api_key"]
    url = Config["base_url"]
    model = Config["model"]
    max_token = Config["max_token"]
    momory_path = Config["momory_path"]

    llm = agent.FrontendAgent(
        key,
        tools=[],
    )
    while True:
        user = prompt_toolkit.prompt("[Xl_AI]< ")
        for i in llm.send_msg(user):
            print("[Xl_AI]>",f"""
            {i}
            """)
        

main()