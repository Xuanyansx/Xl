"""Xl_AI test6 Web 前端入口

把 Agent.send() 的事件流包装成 NDJSON 流给前端消费。

运行：
    cd test6
    ../ai_venv/bin/python webui.py
然后打开 http://127.0.0.1:8000

事件协议（每一行一个 JSON）：
    {"type":"user",  "content": str}
    {"type":"bot",   "content": str, "think": str}
    {"type":"tool",  "name": str, "args": obj, "res": str,
                     "time": str, "prompt": str, "is_work": bool|None}
    {"type":"todo",  "todo": {...}}
    {"type":"error", "message": str}
    {"type":"done"}
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, Response, request, send_from_directory, stream_with_context

import custom_structs as st
import agent as agent_mod
from xl_config import config as cfg


app = Flask(__name__, static_folder="static")

_agent = None


def get_agent():
    """懒创建 Agent：同一个实例跨多轮对话，保留连续上下文。"""
    global _agent
    if _agent is None:
        C = cfg.Config
        _agent = agent_mod.Agent(
            C["api_key"],
            C["base_url"],
            C["model"],
            C["max_token"],
            C["max_active_turn"],
            C["max_turn"],
            C["work_TTL"],
        )
    return _agent


def todo_to_dict(todo):
    return {
        "id": todo.id,
        "title": todo.ttitle,
        "description": todo.description,
        "status": todo.status,
        "running_id": todo.running_id,
        "create_time": todo.create_time,
        "tasks": [
            {
                "id": t.id,
                "title": t.ttitle,
                "content": t.content,
                "status": t.status,
            }
            for t in todo.tasks
        ],
        "notes": list(todo.task_notes or []),
    }


def extract_todo(raw):
    """从 ToolRes 里挖 TodoRes / Todo，转成前端友好的 dict。"""
    res = getattr(raw, "todo_res", None) or getattr(raw, "_res", None)
    if isinstance(res, st.TodoRes) and res.todo is not None:
        return todo_to_dict(res.todo)
    if isinstance(res, st.Todo):
        return todo_to_dict(res)
    return None


def json_safe(v):
    """把任意对象降级成可 JSON 序列化的结构。

    工具的返回值完全由工具自己决定，可能是 bytes（比如 rg 没有匹配到内容时
    返回的 {"stdout": b"", "stderr": b""}）、set、异常对象之类的东西。
    在事件流的出口统一处理，避免整条 NDJSON 流挂在 json.dumps 上。
    """
    if v is None or isinstance(v, (bool, int, float, str)):
        return v
    if isinstance(v, bytes):
        return v.decode("utf-8", errors="replace")
    if isinstance(v, (bytearray, memoryview)):
        return bytes(v).decode("utf-8", errors="replace")
    if isinstance(v, dict):
        return {str(k): json_safe(val) for k, val in v.items()}
    if isinstance(v, (list, tuple, set, frozenset)):
        return [json_safe(i) for i in v]
    return str(v)


def safe_str(v):
    v = json_safe(v)
    if isinstance(v, str):
        return v
    if isinstance(v, (dict, list)):
        return json.dumps(v, ensure_ascii=False, indent=2)
    return str(v)


def event_stream(message):
    yield {"type": "user", "content": message}
    try:
        agent = get_agent()
        for ev in agent.send(message):
            if ev["type"] == "bot":
                body = ev.get("body", {})
                yield {
                    "type": "bot",
                    "content": body.get("msg") or "",
                    "think": body.get("think") or "",
                }
            elif ev["type"] == "tool":
                body = ev.get("body", {})
                raw = ev.get("raw_data")
                yield {
                    "type": "tool",
                    "name": body.get("name"),
                    "args": body.get("args"),
                    "res": safe_str(body.get("res")),
                    "time": body.get("time", ""),
                    "prompt": ev.get("prompt") or "",
                    "is_work": ev.get("is_work"),
                }
                # Agent.send 已尽量在事件里带 todo，这里兜底再挖一次
                todo = ev.get("todo")
                if todo is not None and not isinstance(todo, dict):
                    todo = todo_to_dict(todo)
                if todo is None:
                    todo = extract_todo(raw)
                if todo:
                    yield {"type": "todo", "todo": todo}
    except Exception as e:
        yield {"type": "error", "message": f"{type(e).__name__}: {e}"}
    finally:
        yield {"type": "done"}


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return {"error": "消息不能为空"}, 400

    def gen():
        for ev in event_stream(message):
            yield json.dumps(ev, ensure_ascii=False) + "\n"

    return Response(
        stream_with_context(gen()),
        mimetype="application/x-ndjson",
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=False)
