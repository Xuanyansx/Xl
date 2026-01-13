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

100	用户	用户已存在=
101	用户	用户不存在=
102	用户	密码错误=
103	用户	信息验证失败
104	用户	注册成功
105	用户	登录成功
106	用户	需要重新登录
107 用户    未注册的用户
108 用户    连接成功，需要用户发送身份数据  

200	通信	成功
201	通信	广播消息
202	通信	私聊消息
203	通信	通信开始
204 通信    文件发送


400 通信    未知消息
401	通信	私聊消息发送失败
402 通信    文件上传失败
403 通信    文件获取失败
404 通信    没有该文件
405 通信    拒绝客户端的请求



500	系统	未知错误或服务器异常


消息格式
type(2b)+头部(4b)+主要数据(json)
00  用户信息    size     {name:name,passwd:passwd}   对于客户端是纯code消息

10  普通消息    size     {who:any ,msg:msg}
11  私聊消息    size     {who:name,msg:msg}

20  上传群发文件    szie     {who:any ,fname:name,fsize:num}     file_bit
21  上传私发文件    size     {who:name,fname:name,fsize:num}     file_bit

30  向服务端发起请求    size    {cmd:cmd,fname:name}


客户端上传文件需服务端同意才能上传
"""


import os
import json
import selectors
import socket as sk
from queue import Queue
from pathlib import Path
from threading import Thread,Lock



ip = "127.0.0.1"
port = 51277

code_str = "UTF-8"
online = [] #[SessionClass]
users = {} #{name:passwd}
file_acl = {}#{file_name:{"owner":name,"allowed":[]}}
online_queue = Queue()
register_queue = Queue()




class UserClass:
    def __init__(self,conn:sk.socket,addr:str):
        self.conn = conn
        self.addr = addr
        self.name = None
        

class SessionClass:
    """
    接收消息处理协议
    发送消息封装协议
    
    """
    def __init__(self,user:UserClass):
        self.conn = user.conn
        self.user = user
    
    def __recv_data(self,size):
        try:
            conn = self.conn
            data = conn.recv(size)
        except Exception as e:
            return False,None
        return True,data

    def __recv_head(self):
        is_ok,data_type = self.__recv_data(2)
        is1_ok,body_size = self.__recv_data(4)
        data_type = data_type.decode(code_str)
        body_size = body_size.decode(code_str)
        if not is_ok or not is1_ok:
            return False,None
        body_size = int(body_size)
        return True,(data_type,body_size)

    def __recv_body(self):
        body = b''
        is_ok,res = self.__recv_head()
        data_type,body_size = res
        if not is_ok:
            return False,None
        while body_size>0:
            chunk_size = min(1024,body_size)
            is_ok,data = self.__recv_data(chunk_size)
            if not is_ok:
                return False,None
            body+=data
            body_size -= chunk_size
        return True,(data_type,json.loads(body.decode(code_str)))
    
    def __recv_file(self,body):
        file_size = body["fsize"]
        fl = FileClass.file_load(body,self.user.name)
        next(fl)
        while file_size>0:
            chunk_size = min(1024,file_size)
            is_ok,data = self.__recv_data(chunk_size)
            if not is_ok:
                return False    
            fl.send(data)
            file_size-=chunk_size
        fl.send(None)
        return True
    
            
    def send_msg(self,code,conn = 'self',msg='',msg_type='1'):
        if conn == 'self':
            conn  = self.conn
        msg_bytes = msg.encode(code_str)
        msg_size = len(msg_bytes)
        msg_head = bytes(str(msg_size),code_str).zfill(4)
        msg_type = bytes(msg_type,code_str).zfill(2)
        conn.send(code.encode(code_str))
        conn.send(msg_type)
        conn.send(msg_head)
        conn.send(msg_bytes)
        #code msg_type body_size body

    def send_file(self,path):
        
        conn = self.conn
        uname = self.user.name
        while True:
            f_ok,code = FileClass.check_file(path=path)
            fname,fsize = FileClass.get_file_info(path)
            if not f_ok:
                break
            a_ok,code = FileClass.check_file(fname=fname,uname=uname)
            if a_ok:
                fr = FileClass.file_read(path,fsize)
                body = str({'fname':fname,'fsize':fsize})
                self.send_msg('204',msg=body,msg_type='2')
                while True:
                    data = next(fr)
                    if data is None:
                        break
                    conn.send(data)
            break
        self.send_msg(code)

    
    def get_msg(self):
        is__ok,res = self.__recv_body()
        if not is__ok:
            return False,None
        data_tyep,body = res
        if data_tyep[0] == '2':
            is_ok, code = FileClass.check_file(
                fname=body["fname"],
                fsize=body["fsize"]
            )
            if is_ok:
                ok = self.__recv_file(body)
                if not ok:
                    return False,None
            self.send_msg(code)
        return True,(data_tyep,body)


class AuthClass:
    @staticmethod
    def __login(name,passwd):
        if users[name] == passwd:
            return True,'105'
        return False,'103'
    
    @staticmethod
    def __register(name,passwd):
        register_queue.put((name,passwd))
        return True,'104'
        

    @classmethod
    def check_auth(cls,name,passwd):
        if name not in users:
            cls.__register(name,passwd)
        code,is_ok = cls.__login(name,passwd)
        return is_ok,code
    
    
    @staticmethod
    def save_users(data):
        pass


class FileClass:
        """
        文件类
        """
        @staticmethod
        def save_file(path,data):
            with open(path,mode='w',encoding=code_str) as f:
                json.dump(data,f)

        @staticmethod
        def check_file(fname='',fsize=0,uname='',path=''):
            global file_acl
            """
            检测文件是否合规
            只允许上传4M以内的文件
            禁止上传.py .js .html .php
            """
            d_size = 4*1024
            d_list = [".py",".js",".html",".php"]
            if fsize >= d_size or any(i in fname for i in d_list):
                return False,'405'
            if file_acl[fname]["allowed"] != 'any' and uname not in file_acl[fname]["allowed"]:
                return False,'405'
            if path and not os.path.exists(path):
                return False,'404'
            
            return True,'200'
        
        @staticmethod
        def get_file_info(file_path):
            """
            获取文件名称和文件大小
            
            参数:
            file_path (str): 文件路径
            
            返回:
            tuple: (文件名称, 文件大小(字节))
                如果文件不存在或不是文件，返回 (None, None)
            """
            try:
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    file_name = os.path.basename(file_path)
                    file_size = os.path.getsize(file_path)
                    return file_name, file_size
                else:
                    return None, None
            except Exception:
                return None, None

        @classmethod
        def file_load(cls,file_body,owner):
            fname = file_body["fname"]
            who = file_body["who"]

            with open(f'file/{fname}',mode='wb') as f:
                while True:
                    data = yield
                    if data is None:
                        break
                    f.write(data)
            cls.w_acl(fname,owner,[owner,who])

        @staticmethod
        def file_read(path,fsize):
            with open(path,mode='rb') as f:
                while fsize>0:
                    chunk_size = min(1024,fsize)
                    data = f.read(chunk_size)
                    yield data
                    fsize-=chunk_size
                yield None

        @classmethod
        def w_acl(cls,file_name,owner,allowed):
            global file_acl
            file_acl[file_name] = {
            "owner": owner,
            "allowed": allowed
            }
            cls.save_file(f'file/config/acl.json',file_acl)

            

            
class MsgClass:
    def __init__(self,user:UserClass):
        self.conn = user.conn
        self.user = user

    def check_msg(self,msg):
        """
        违禁词检测与替换
        """
        pass
    

    def broadcast(self,msg):
        for i in online:  
            pass
            
    
    def unicast(self,msg,to_name):
        pass        


def msg_loop(user:UserClass,session:SessionClass,message:MsgClass):
    """
    通信循环（处理
    还得是if大法，不是不想优化，，，，其实就是懒得优化了... (25/12/4)  
    """
    is_ok,msg_d=session.get_msg()
    if not is_ok:
        user.conn.close()
        sel.unregister(user.conn)
        return
    msg_type,msg_data = msg_d
    if msg_type == '00':
        name = msg_data['name']
        passwd = msg_data['passwd']
        auth_ok,code = AuthClass.check_auth(name,passwd)
        session.send_msg(code)
        if auth_ok:
            session.send_msg('203')
    if msg_type[0] == '1':
        who = msg_data["who"]
        msg = msg_data["msg"]
        msg = message.check_msg(msg)
        if msg_type[1] == '0':
            message.broadcast(msg)
        else:
            message.unicast(msg,who)
    if msg_type[0] == '2':
        who = msg_data["who"]
        fname = msg_data["fname"]
        fize = msg_data["fsize"]
        if msg_type[1] == '0':
            msg = f'用户 {user.name} 分享了 {fname} 大小 {fize/1024}m \n 输入download {fname} 即可下载'
        else :
            msg = f'用户 {user.name} 向您分享了 {fname} 大小 {fize/1024}m \n 输入download {fname} 即可下载'
        message.broadcast(msg)
    if msg_type == '30':
        cmd = msg_data['cmd']
        if cmd == 'download':
            fname == msg['fname']
            path = f'filr/{fname}'  
            session.send_file(path)
        


def client_connect(servre:sk.socket):
    conn,addr = servre.accept()
    user_class = UserClass(conn,addr)
    session = SessionClass(user_class)
    message = MsgClass(user_class)
    sel.register(user_class.conn,selectors.EVENT_READ,lambda _: msg_loop(user_class,session,message))


if __name__ == "__main__":

    if not os.path.exists("users.json"):
        with open("users.json","w",encoding=code_str) as f:
            f.write("{}")

    Path('file').parent.mkdir(parents=True,exist_ok=True)
    Path('file/config').parent.mkdir(parents=True,exist_ok=True)

    with open('users.json',mode='r',encoding=code_str) as f:
        users = json.load(f)

    with open('file/config/acl.json',mode='r',encoding=code_str) as f:
        file_acl = json.load(f)


    servre = sk.socket()
    servre.bind((ip,port))
    servre.listen(10)
    
    sel = selectors.DefaultSelector()
    servre.setblocking(False)
    sel.register(servre,selectors.EVENT_READ,client_connect)

    while True:
        rlist = sel.select()
        for key,en in rlist:
            func = key.data
            func(key.fileobj)




"""
私聊功能
公屏聊天
文件上传与下载




hhhhhh,有点风格不统一了

放弃了，等学完全部的课程再来重构吧，学一个知识点就马上来实操还是有点不太好，原因无他这写出来的东西太奇怪了
风格上的不统一，前面想出的东西，后面写完发现不可取就打补丁，，，结果呢代码逻辑越来越混乱，越感觉之前设计
出来的类、函数这些的非常不好，简直不想是一个人写出来的（   25/12/6
"""
    