# 2026/11/01 18:10: ai生成的，懒得写了

"""集中类型出口。

任何模块都可以从这里 import 项目公共类型，不必记住每个类住在哪个文件::

    from __future__ import annotations
    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from xlagent.types import ContextManager, ToolManager, LLMClient, AgentConfig

注意：本文件只在类型检查阶段被读取（``TYPE_CHECKING`` 运行时为 False），
因此它内部的循环引用不会造成运行时问题，也不会把 openai 之类的重依赖
带进启动路径。**不要**在运行时 import 它。

要加新类型，直接在下面补一行即可。

"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # 运行时组件
    from xlagent.core.config import Config
    from xlagent.core.context import ContextManager
    from xlagent.core.loop import Agent
    from xlagent.core.tool import ToolManager
    from xlagent.llm.client import LLMClient

    # 配置数据类（structs/options.py），加 Config 后缀区分“配置”和“组件”
    from xlagent.structs.options import LLM as LLMConfig
    from xlagent.structs.options import CTX as CTXConfig
    from xlagent.structs.options import Tool as ToolConfig
    from xlagent.structs.options import Agent as AgentConfig
