## 核心话题
1. VulnClaw skill 加载机制分析：
   - skill 内容通过 system prompt 每轮重建注入（非对话历史）
   - dispatcher 只返回一个最高分 skill，其他命中的 skill 被浪费
   - auto 模式下 auto_skill_input 固定，skill 不会随阶段变化切换
   
2. 设计方向讨论：
   - 当前问题：多任务时只注入一个 skill，其他 skill 知识被丢弃
   - AI 自主按需加载 skill（类似记忆系统的热插拔模式）
   - 兼容 VulnClaw 的 skill 格式（markdown + 目录结构）作为基础标准
   - 目标是让 AI 在需要时主动调用工具加载 skill，用完即弃

3. 当前卡点：
   - xuanyansx 想做得太通用，兼容所有 skill 格式
   - 但市面上 skill 安装方式各异，没有统一标准
   - 定义自己的标准至少需要兼容一款现有格式

4. 关键结论：
   - VulnClaw skill 格式很简单：SKILL.md + references/ 目录
   - 直接兼容 VulnClaw 格式成本几乎为零
   - 加上 AI 自主按需加载 + 热插拔机制就是 Weave 的 skill 系统