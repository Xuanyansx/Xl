def format_message(msg):
    """
    处理单条 OpenAI 格式消息，返回格式化后的字符串。
    兼容 dict 和对象两种消息类型，无业务耦合。
    """
    def _get_field(obj, field, default=""):
        if isinstance(obj, dict):
            return obj.get(field, default)
        return getattr(obj, field, default)

    role = _get_field(msg, "role")
    content = _get_field(msg, "content", "")
    name = _get_field(msg, "name", "")      # 变种 user 消息的标识（即 prompt_presets 的 key）

    result = ""

    if role == "user":
        if name:
            result = f"role[{name}]：{content}"
        else:
            result = f"用户：{content}"

    elif role == "assistant":
        parts = []
        tool_calls = _get_field(msg, "tool_calls", [])
        if tool_calls:
            for tool in tool_calls:
                tool_id = _get_field(tool, "id", "")
                function = _get_field(tool, "function", {})
                func_name = _get_field(function, "name", "")
                func_args = _get_field(function, "arguments", "")
                parts.append(f"调用工具：{func_name},id:{tool_id},  参数：{func_args}")
        if content:
            parts.append(f"回复：{content}")
        result = "助手" + "；".join(parts) if parts else ""

    elif role == "tool":
        call_id = _get_field(msg, "tool_call_id", "")
        result = f"工具 {call_id} 返回：{content}"

    elif role == "system":
        result = f"系统：{content}"

    return result + "\n"