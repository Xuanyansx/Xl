import agent_fork as agent
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

    llm = agent.Agent(
        key,
        tools=[],
        base_url=url,
        modle=model
    )
    while True:
        user = prompt_toolkit.prompt("[Xl_AI]< ")
        for i in llm.send(user):
            print("[Xl_AI]>")
            if i["type"] == "bot":
                print(i["body"]["msg"])
                print(i["raw_data"]) 
            else:
                print(i["body"]["name"])
                print(i["body"]["args"])
                print("is_work=>>>>",i["is_work"])
                print(i["todo"])
                print(i["raw_data"]) 

main()