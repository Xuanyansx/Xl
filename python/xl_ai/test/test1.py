from openai import OpenAI
import subprocess
import prompt_toolkit
import json


c = OpenAI(
    api_key="sk-54e96e93441647938ac1986980e7ed3f",
    base_url="https://api.deepseek.com",
)

h = {}

messages=[
    {"role":"system","content":"扮演人类的bot"}
]

def send_msg(message):
    res = c.chat.completions.create(
        model="deepseek-v4-flash",
        messages=messages,
        tools=[
            {
                "type":"function",
                "function":{
                    "name":"test_func",
                    "description":"当对话中明确要求使用测试工具时使用"
                }
            },
            {
                "type":"function",
                "function":{
                    "name":"run_shell_cmd",
                    "description":"使用shell执行命令",
                    "parameters":{
                        "type": "object",
                        "properties": {
                            "cmd": {"type": "string", "description": "要执行的 shell 命令"}
                        },
                        "required": ["cmd"]
                    },
                }
            }
        ]   
    )
    return res

def run_shell_cmd(*args,**kwargs):
    res = subprocess.run(json.loads(args[0])["cmd"],capture_output=True,text=True,shell=True)
    return {"stderr":res.stderr,"stdout":res.stdout,"returncode":res.returncode}

def test_t(*args,**kwargs):
    return "ok"


func_tools = {
    "run_shell_cmd":run_shell_cmd,
    "test_func":test_t
}

while True:
    messages.append({"role":"user","content":prompt_toolkit.prompt("< ")})
    res = send_msg(messages)
    msg = res.choices[0].message
    messages.append(msg)

    print(f"> {msg.content}\n")
    # print(f"思考内容 :{msg.reasoning_content}\n")

    if msg.tool_calls:
        tools = msg.tool_calls
        for tool in tools:

            tool_name = tool.function.name
            tool_id = tool.id
            canshu = tool.function.arguments

            ress = func_tools[tool_name](canshu)
            messages.append(
                {
                "role":"tool",
                "tool_call_id":tool_id,
                "content":f"执行结果{ress}"
                }
            )
            print(f">>>{canshu}<<<")
        res = send_msg(messages)
        print(res.choices[0].message.content)



# arguments =
# '{"cmd": "uname -a"}'



      
# print("=="*50)
# msg = res.choices[0].message
# print(msg.content)
# print(f"思考内容 :{msg.reasoning_content}")
# print("= "*10)
# print(msg)


# 成了！！，算是一个半成品的智能体了，第一次写成啊，hh 26/6/18