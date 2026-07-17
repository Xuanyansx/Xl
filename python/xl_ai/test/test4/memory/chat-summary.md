【对话摘要 2026/07/03】
1. 获取了第一个CTF flag (ctfshow{42e6ef1a...}) — 页面HTML注释藏Base64
2. 测试了所有Burp工具，全部正常工作
3. 发现Burp HTTP请求偶尔超时，排查原因是mcp-proxy.jar有30秒硬编码超时
4. 又获取了第二个CTF flag (ctfshow{be6eef70...}) — web2 SQL注入题，UNION注入从flag表查出
5. 发现Burp POST超时的真正原因是手写Content-Length不准确，修正后正常
6. 用户结论：怎么方便怎么来，Kali curl发请求，Burp用特色功能
## 八卦星图馆挑战进度 (2026/07/08 ~07:42)

**已完成：**
1. ☰ 乾卦 (入门求测) ✅ - MongoDB NoSQL注入，以 qingyun 登录
2. ☱ 兑卦 (自修门规) ✅ - MongoDB字段注入，成功将role从apprentice改为elder/master

**卡住：**
3. ☲ 离卦 (抢头香) - 需要3张令牌才能进震卦。Race condition题，已抢1张但错过了并发窗口。"每人限1张今日已领过"。需要重置状态或用其他方法拿令牌。
4. ☳ 震卦 (占天机签) - 已成功用z3破解xorshift128+预测随机数（第N期），但需要3张令牌才能提交预测。

后四卦（☴巽☵坎☶艮☷坤）待启。

**关键发现：**
- 半仙碎碎念 `/half-immortal` 提示"钥匙藏在了源码里"
- robots.txt 暴露了 `/half-immortal` 和 `/admin/`
- 兑卦更新接口可以添加任意字段到用户文档
