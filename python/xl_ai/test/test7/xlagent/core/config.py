import os
import json
from dotenv import load_dotenv
from xlagent.structs import options

load_dotenv()
env_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")

class Config:
    def __init__(self,path):
        self.is_init = False
        if os.path.exists(path):
            self.is_init = True

            with open(path,'r') as f:
                data = json.load(f)
                print(data)

            key = data['llm']["api_key"] if data['llm']["api_key"] else env_key
            self.llm = options.LLM(
                api_key=key,
                base_url=data['llm']["base_url"],
                model=data['llm']["model"]
            )
            self.tool = options.Tool()
            self.ctx = options.CTX()
            self.agent = options.Agent()

    def init(self):
        ...



if __name__ == "__main__":
    Config("/home/xuanyansx/Desktop/Xl/python/xl_ai/test/test7/data/config/config.json")


    
    