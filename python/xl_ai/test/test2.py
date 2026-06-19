from openai import OpenAI
import subprocess
import prompt_toolkit
import json
from rich.console import Console
from rich.markdown import Markdown

# 创建 Rich Console 对象
console = Console()

c = OpenAI(
    api_key="sk-54e96e93441647938ac1986980e7ed3f",
    base_url="https://api.deepseek.com",
)


messages=[
    {"role":"system","content":"努力扮演人类的bot"}
]

tools = [
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

def send_msg(message):
    res = c.chat.completions.create(
        model="deepseek-v4-flash",
        messages=messages,
        tools=tools
    )
    return res

def run_shell_cmd(args):
    res = subprocess.run(args["cmd"],capture_output=True,text=True,shell=True)
    return {"stderr":res.stderr,"stdout":res.stdout,"returncode":res.returncode}

def test_t(args):
    return "ok"


func_menu = {
    "run_shell_cmd":run_shell_cmd,
    "test_func":test_t
}


while True:
    messages.append(
        {
            "role":"user",
            "content":prompt_toolkit.prompt("[Xl_AI]< ")
        }
    )
    reply_message = send_msg(messages).choices[0].message
    # print(f"[Xl_AI]> {reply_message.content}")
    console.print(Markdown(reply_message.content))
    messages.append(reply_message)

    while reply_message.tool_calls:
        user_tools = reply_message.tool_calls
        for tool in user_tools:

            tool_name = tool.function.name
            tool_id = tool.id
            canshu = json.loads(tool.function.arguments)

            print(f"\t[run]> {canshu}")
            res = func_menu[tool_name](canshu)
            messages.append(
                {
                    "role":"tool",
                    "tool_call_id":tool_id,
                    "content":f"{res}"
                }
            )

        reply_message = send_msg(messages).choices[0].message
        messages.append(reply_message)
        # print(f"[Xl_AI]> {reply_message.content}")
        console.print(Markdown(reply_message.content))






# 多轮工具的使用也是之间写出来了 26/6/19

# while True:
#     messages.append({"role":"user","content":prompt_toolkit.prompt("< ")})
#     res = send_msg(messages)
#     msg = res.choices[0].message
#     messages.append(msg)

#     print(f"> {msg.content}\n")
#     # print(f"思考内容 :{msg.reasoning_content}\n")

#     if msg.tool_calls:
#         tools = msg.tool_calls
#         for tool in tools:

#             tool_name = tool.function.name
#             tool_id = tool.id
#             canshu = tool.function.arguments

#             ress = func_menu[tool_name](canshu)
#             messages.append(
#                 {
#                 "role":"tool",
#                 "tool_call_id":tool_id,
#                 "content":ress
#                 }
#             )
#             print(f">>>{canshu}<<<")
#         res = send_msg(messages)
#         print(res.choices[0].message.content)


