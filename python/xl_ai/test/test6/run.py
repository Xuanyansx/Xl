import agent as agent
import xl_mcp.mcp_cs
import prompt_toolkit
import xl_config.config as c
# import xl_config.mcp_config as 



class mcp:
    tools = []
    failed_tools = []

class skill:
    skill_index = []

class soul:
    ...

def main():
    Config = c.Config
    # config = Config
    key = Config["api_key"]
    url = Config["base_url"]
    model = Config["model"]
    max_token = Config["max_token"]
    max_turn = Config["max_turn"]
    max_active_turn = Config["max_active_turn"]
    gc_turn = Config["gc_turn"]
    # momory_path = Config["momory_path"]

    llm = agent.Agent(
        key,
        url,
        model,
        max_token,
        max_active_turn,
        max_turn,
        gc_turn,
        []
    )

    llm.tools = mcp.tools
    llm.skill = skill.skill_index
    llm.soul = soul

    while True:
        user = prompt_toolkit.prompt("[Xl_AI]< ")
        for i in llm.send(user):
            print("[Xl_AI]>")
            print(i)
            # if i["type"] == "bot":
            #     print(i["body"]["msg"])
            #     print(i["raw_data"]) 
            # else:
            #     print(i["body"]["name"])
            #     print(i["body"]["args"])
            #     print("is_work=>>>>",i["is_work"])
            #     print(i["todo"])
            #     print(i["raw_data"])

main()