#
#                       _oo0oo_
#                      o8888888o
#                      88" . "88
#                      (| -_- |)
#                      0\  =  /0
#                    ___/`---'\___
#                  .' \\|     |# '.
#                 / \\|||  :  |||# \
#                / _||||| -:- |||||- \
#               |   | \\\  -  #/ |   |
#               | \_|  ''\---/''  |_/ |
#               \  .-\__  '-'  ___/-. /
#             ___'. .'  /--.--\  `. .'___
#          ."" '<  `.___\_<|>_/___.' >' "".
#         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
        # \  \ `_.   \_ __\ /__ _/   .-` /  /
#     =====`-.____`.___ \_____/___.-`___.-'=====
#                       `=---='
#
#
#     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#               佛祖保佑         永无BUG
#
#
#


"""

users.json

{
    name:passwd,
    ...
}

000	通用	无效请求

100	用户	用户已存在
101	用户	用户不存在
102	用户	密码错误
103	用户	信息验证失败
104	用户	注册成功
105	用户	登录成功
106	用户	需要重新登录
107 用户    未注册的用户
108 用户    用户需发送用户信息  

200	通信	通信通道建立成功（开始聊天）
201	通信	广播消息
202	通信	私聊消息
203	通信	同步在线列表
204	通信	私聊消息发送成功

400	通信	私聊消息发送失败

500	系统	未知错误或服务器异常



服务端接收的消息格式
type(2b)+头部(4b)+主要数据(json)
00  用户信息    size     {name:name,passwd:passwd}
01  普通消息    size     {who:all ,msg:msg}
02  私聊消息    size     {who:name,msg:msg}
03  群发文件    szie     {who:all ,fname:name,fsize:num}     file_bit
04  私发文件    size     {who:name,fname:name,fsize:num}     file_bit



"""


import os
import json
import selectors
import socket as sk
from queue import Queue
from threading import Thread,Lock


ip = "127.0.0.1"
port = 51277

online_lock = Lock()
code_str = "utf-8"
online = {}#{name:user}
users = {}


class UserClash:
    def __init__(self,conn,addr) -> None:
        self.conn = conn
        self.addr = addr
        self.name = '未注册'

    def login(self,passwd):
        name = self.name
        if name not in users:
            return False, 101  # 没有用户
        if passwd != users[name]:
            return False, 102  # 密码错误
        if passwd == users[name]:
            return True, 105   # 登录成功
        return False, 103      # 信息验证失败
    
    def register(self,name):
        if name in users:
            return False, 100  # 用户已存在
        self.name = name
        return True, 104       # 注册成功 
    

    def recv_data(self):
        conn = self.conn
        msg = b''
        data_type = conn.recv(2)
        data_size = conn.recv(4)
        msg_len = int(data_size.decode(code_str))
        msg_type = int(data_type.decode(code_str))

        if msg_type>2:
            file_head = conn.recv(msg_len)
            return ("file",file_head)

        while msg_len > 0:
            chunk_size = min(1024,msg_len)
            data = conn.recv(chunk_size)
            msg_len -= chunk_size
            msg+=data
        return ("msg",msg)
    
    def send_data(self,code,msg=''):
        pass

    def recv_file(self,file_size):
        conn = self.conn
        while file_size>0:
            chunk_size = min(1024,file_size)
            data = conn.recv(chunk_size)
            yield data
            file_size -= chunk_size
        yield b''
    
    def download(self,file_name):
        pass

def save_users(data):
    with open("users.json",mode='w',encoding=code_str) as f:
        json.dump(data,f)

def download(file_name,who):
    with open(file_name,'wb') as f:
        while True:
            file_data = yield
            if not file_data:
                break
            f.write(file_data)

def broadcast(msg,f,code):
    for name,u in online.items():
        if f == name:
            continue
        u.send_data(code,msg)

def send_msg(msg,code,who,user:UserClash):
    name = user.name
    if who == "all":
        broadcast(msg,name)
    else :
        if who in online:
            online["who"].send_data(code,msg)
            



def task(user:UserClash):
    while True:
        user.send_data(108)
        t,uinfo = user.recv_data()
        uinfo = uinfo.decode(code_str)
        name = uinfo["name"]
        passwd = uinfo["passwd"]

        if name not in users:
            is_true,code = user.register(name,passwd)
        else :
            user.name = name
            is_true,code = user.login(passwd)
        
        user.send_data(code)
        if not is_true:
            continue
        break

    user.send_data(200)
    msg_type,msg = user.recv_data()
    head = json.loads(msg.decode(code_str))

    if msg_type == "file":
        file_name = head["fname"]
        file_size = head["fsize"]
        fwho = head["who"]

        frecv = user.recv_file(file_size)
        fdownload = download(file_name,fwho)
        next(fdownload)

        for chunk in frecv:
            fdownload.send(chunk)
    if msg_type == "msg":
        who = head["who"]
        msg = head["msg"]
    


    
def user_join(server:sk.socket):
    conn,addr = server.accept()
    print(f"主机 @{addr}连接成功")

    user = UserClash(conn,addr)
    sel.register(user.conn,selectors.EVENT_READ,lambda _:task(user))


if __name__ == "__main__":

    if not os.path.exists("users.json"):
        with open("users.json","w",encoding=code_str) as f:
            f.write("{}")

    with open('users.json',mode='r',encoding=code_str) as f:
        users = json.load(f)
    
    print("服务端启动成功！")
    server = sk.socket()
    server.bind((ip,port))
    sel = selectors.DefaultSelector()
    sel.register(server,selectors.EVENT_READ,user_join)

    while True:
        rlist = sel.select()

        for key,en in rlist:
            func = key.data
            func(key.fileobj)   



"""
私聊功能
公屏聊天
文件传输


"""
    