## 核心话题
1. VulnClaw 项目分析：Skill体系（7核心+14专项）、意图引擎（SKILL_INTENT_MAP关键词打分+1.5x加权）、工作循环（auto_pentest双层循环+SessionState状态管理）、上下文管理（build_round_context状态摘要 + _fit_context_window滑动窗口截断）
2. Weave（test4）自我审视：发现Skill系统只有注释占位符、记忆卸载未完成、digest_chat触发阈值过高（30万token）、缺少中间状态管理层
3. 重构方向讨论：借鉴VulnClaw的SessionState/SkillDispatcher/阶段管理，保留digest_chat的LLM摘要压缩优势

## 关键结论
- Weave的名字来源于前一代Nexus的猜想（Loom/织机）
- 行为规范：禁止用shell直接读memory/目录（已踩坑记录）
- 重要信息已建立独立记忆索引
- 用户打算在测试完成后重构Weave代码

## 调用的工具/功能
- run_shell：扫描VulnClaw源码、读取test4项目文件
- list_memory_index / load_memory：查询记忆索引和行为规范
- edit_long_memory：更新长期记忆（记录教训）
- add_memory：创建重要信息索引

## 未完成任务
- 后续需要实现Skill系统的 skill_list/skill_load 工具接口
- 上下文压缩函数的具体实现方案待定

## 待办事项
- [Weave] 主动保存对话摘要到记忆，避免程序关闭后丢失
- [Weave] 降低digest_chat触发阈值，或改为定期主动压缩
