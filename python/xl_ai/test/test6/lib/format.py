

def _get(msg, key, default=None):
    """消息要么是 dict（user/tool/system），要么是 SDK 对象（assistant）。"""
    if isinstance(msg, dict):
        return msg.get(key, default)
    return getattr(msg, key, default)


def format_message(msg):
    """把一条消息格式化成一行文本，结尾带换行。

    user/tool/system 传 dict，assistant 传 SDK 的 ChatCompletionMessage 对象。
    """
    role = _get(msg, "role")
    content = _get(msg, "content") or ""

    if role == "user":
        name = _get(msg, "name")
        return f"role[{name}]：{content}\n" if name else f"用户：{content}\n"

    if role == "assistant":
        parts = [
            f"调用工具：{t.function.name},id:{t.id},  参数：{t.function.arguments}"
            for t in _get(msg, "tool_calls") or []
        ]
        if content:
            parts.append(f"回复：{content}")
        return "助手" + "；".join(parts) + "\n"

    if role == "tool":
        return f"工具 {_get(msg, 'tool_call_id')} 返回：{content}\n"

    if role == "system":
        return f"系统：{content}\n"

    return ""

# 懒得写这个功能了（上面的代码），给ai写了，反正我也会写，偷懒这一块 2026/09/16 16:59:



