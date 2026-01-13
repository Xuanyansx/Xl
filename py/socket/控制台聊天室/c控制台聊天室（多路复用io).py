"""

客户端发送的消息
type(2b)+头部(4b)+主要数据(json)
00  用户信息    size     {name:name,passwd:passwd}

10  普通消息    size     {who:all ,msg:msg}
11  私聊消息    size     {who:name,msg:msg}

20  上传群发文件    szie     {who:all ,fname:name,fsize:num}     file_bit
21  上传私发文件    size     {who:name,fname:name,fsize:num}     file_bit

30  下载文件        size    {fname:name}

"""

