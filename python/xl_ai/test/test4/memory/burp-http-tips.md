【Burp HTTP请求注意事项】
1. Content-Length 必须精确，手写容易算错字节数导致服务器一直等待超时
2. Kali curl 自动计算 Content-Length，更省心
3. Burp 工具有时候请求外网会超时（mcp-proxy.jar 30s限制），Kali curl 无此限制
4. 最佳实践：需要 Burp 特色功能（编码/Repeater/Intruder/扫描）时用 Burp；单纯发HTTP请求用 Kali curl
5. 已实测验证：Burp 的 GET 和 POST 都能正常工作，前提是 Content-Length 正确