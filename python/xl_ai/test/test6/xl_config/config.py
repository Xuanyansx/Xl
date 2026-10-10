# /home/xuanyansx/Desktop/Xl/python/xl_ai/test/test6/xl_config/config.py

import os
from dotenv import load_dotenv

load_dotenv()

env_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")


Config = {
    "api_key": env_key if env_key else "",  # 空时自动用 .env 的
    "base_url": "https://api.deepseek.com",
    # "base_url":"http://192.168.2.116:8765/v1",
    # "model" : "deepseek-reasoner",
    "model" : "deepseek-v4-flash",
    "max_token" : 700000,
    "max_active_turn" : 20,
    "max_turn" : 50,
    "work_TTL" : 3,
    "load_tools" : [],
}

if __name__ == "__main__":
    print(env_key)

    