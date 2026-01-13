




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

状态码
0000   未注册
0001   用户存在
0002   没有用户
0003   密码错误
0004   信息验证失败
0005   注册成功
0006   登录成功
0007   请求用户信息
0008   重新登录
0009   通信开始
0010   广播消息
0011   私聊消息
0012   同步在线列表
0013   私聊消息发送失败
0014   私聊消息发送成功

 
协议
服务端对客户端发送数据
    状态码(4B)+头部(4B)+主要数据
        头部(主要数据的长度)

客户端对服务端发送消息
    头部(4B)+主要数据

    
私聊
    客户端发送消息 @xxx msg



"""


import os
import json
import time
import socket as sk
from queue import Queue
from prompt_toolkit import prompt
from threading import Thread,Lock,active_count
from prompt_toolkit.completion import WordCompleter
# from multiprocessing import Process,Value,active_children,Event


users = {}
online = []
user_map = {}
online_lock = Lock()
user_queue = Queue()
login_queue = Queue()
logout_queue = Queue()


if not os.path.exists("users.json"):
    with open("users.json","w",encoding="utf-8") as f:
        f.write("{}")


class UserClash:
    def __init__(self,name,att) -> None:
        self.name = name
        self.conn = att[0]
        self.addr = att[1]


def save_users(data):
    with open("users.json",mode='w',encoding="utf-8") as f:
        json.dump(data,f)


def change_onlien(is_add,user):
    global online
    online_lock.acquire()
    # print(is_add)
    online.append(user) if is_add else online.remove(user)
    broadcast('0012',str([i.name for i in online]))
    online_lock.release()
    

def thread_w_users():
    global users
    name,passwd = "",""
    user_list = []
    last_time = time.time()
    while True:
        user = user_queue.get()
        user_list.append(user)
        for i in user_list:
            name,passwd = i[0],i[1]
            users[name] = passwd

        if user_list.__len__() == 10:
            save_users(users)
        
        if user_list and (time.time()-last_time>=10):
            # print(users)
            # print(user_list)
            save_users(users)
        

def check_user_reg(name,passwd):
    name = name.decode("utf-8")
    passwd = passwd.decode("utf-8")
    if name in users:
        return False,'0001' #用户存在
    
    user_queue.put([name,passwd])
    return True,'0005' #注册成功


def check_user_login(name,passwd):
    name = name.decode("utf-8")
    passwd = passwd.decode("utf-8")
    
    if name not in users:
        return False,'0002' #没有用户
    if not passwd == users[name]:
        return False,'0003' #密码错误
    if users[name] == passwd:
        return True,'0006' #登录成功
    return False,'0004' # 信息验证失败


def recv_data(conn,var_num):
    res = []
    for i in range(var_num):

        try:
            data = conn.recv(4)
        except Exception as e:
            # if e == "ConnectionAbortedError":
            return False,*([None]*var_num)
        if not data:
            return False,*([None]*var_num)
        msg_size = int(data.decode('utf-8'))
        
        msg = conn.recv(msg_size)
        res.append(msg)
    
    return True,*res


def send_data(conn,code,msg=''):
    msg_bytes = msg.encode('utf-8')
    msg_size = len(msg_bytes)
    msg_head = bytes(str(msg_size),'utf-8').zfill(4)
    # print("~~~+++++===",msg_bytes,msg_head,msg_size)
    conn.send(code.encode("utf-8"))
    conn.send(msg_head)
    conn.send(msg_bytes)


def user_reg(name,passwd,conn,addr):
    res = check_user_reg(name,passwd)
    send_data(conn,res[1])
    if not res[0]:
        return False
    print(f"{addr} 注册成功! 名称 {name.decode('utf-8')}") # type: ignore
    send_data(conn,'0008') #重新登录    
    return True


def user_login(name,passwd,conn,addr):
    res = check_user_login(name,passwd)
    send_data(conn,res[1])
    if not res[0] :
        return False
    print(f"{name.decode('utf-8')} 登录成功 地址 {addr}") # type: ignore

    return True

def broadcast(code,msg,name=None):
    # print(name,msg)
    # print(online)
    """
    如果name有值，就广播除名字以外的的用户
    如果没有值就广播全部人
    """
    # print(msg,code)
    for i in online:
        # print(i.name == name)
        if name and name == i.name:
            continue
        send_data(i.conn,code,msg)


def send_private(name, receiver, msg):
    for i in online:
        if receiver == i.name:
            # print(i.name)
            conn = i.conn
            data = f"用户{name} 悄悄地对你说 {msg}"
            # print(name,receiver,msg)
            send_data(conn,'0011',data)
            return True
    return False
    

def task(conn,addr):
    user_c = None
    is_reg = True
    is_login = False
    is_leave = False
    is_true = None
    
    while True:
        # try:
        send_data(conn,'0007')
        is_true,name,passwd = recv_data(conn,2)
        # print(is_true)
        if not is_true:
            break
        is_in_users = name.decode("utf-8") in users # type: ignore


        if not is_in_users and is_reg:
            send_data(conn,'0000') #用户未注册
            if user_reg(name,passwd,conn,addr):
                is_reg = False
            continue
        else:
            if user_login(name,passwd,conn,addr):
                is_login = True
                user_c = UserClash(name.decode("utf-8"),[conn,addr]) # type: ignore
                login_queue.put(user_c)

            else :
                continue
        send_data(conn,'0009')
        while not is_leave:
            is_true,data = recv_data(conn,1)
            if not is_true:
                break
            msg = data.decode('utf-8')
            n = name.decode("utf-8")
            data = f"{n} >{msg}"

            if msg.startswith('@') and '$' in msg:
                parts = msg.split('$', 1)
                fname = parts[0][1:]
                msg_content = parts[1].strip() if len(parts) > 1 else ''
                # print(msg_content)
                if send_private(n,fname,msg_content):
                    send_data(conn,'0013')
                else :
                    send_data(conn,'0014')
            else:
                broadcast('0010',data,n)

        print("客户端异常退出")
        is_leave = True
        break
    if is_login and is_leave:
        # print(user_c)
        # print(user_c.name) # type: ignore
        logout_queue.put(user_c)

    conn.close()
            

def thread_client_join():
    server = sk.socket()
    server.bind(("127.0.0.1",51277))
    server.listen(10)
    print("服务端启动,等待客户端连接...")

    while True:
        conn,addr = server.accept()
        print(f"主机{addr}已连接")
        
        p = Thread(target=task,args=(conn,addr))
        p.daemon = True
        p.start()
        # conn.send()


def thread_client_login():
    while True:
        user = login_queue.get()
        change_onlien(True,user)


def thread_client_logout():
    while True:
        user = logout_queue.get()
        # print(user)
        change_onlien(False,user)
        

if __name__ == "__main__":   
    with open('users.json',mode='r',encoding="utf-8") as f:
        users = json.load(f)

    
    client_thread = Thread(target=thread_client_join)
    client_thread.daemon = True
    client_thread.start()


    w_users_thread = Thread(target=thread_w_users)
    w_users_thread.daemon = True
    w_users_thread.start()


    client_leave_thread = Thread(target=thread_client_logout)
    client_leave_thread.daemon = True
    client_leave_thread.start()


    client_login_thread = Thread(target=thread_client_login)
    client_login_thread.daemon = True
    client_login_thread.start()
    # def print_onlne():
    #     for i in online


    cmds = {
        "list":lambda : print(*(i.name for i in online),sep='\n'), # type: ignore
        "help":lambda : print("\nlist :显示在线的用户\nexit 退出服务端\nhelp 查看帮助\nthread 查看活跃线程"), #连子命令都没有，看个dan的帮助（，也就看个全部（3个命令）命令（笑 /25/8/3
        "exit":lambda : os._exit(0),
        "thread":lambda : print(active_count())
    }


    command_completer = WordCompleter(list(cmds.keys()), ignore_case=True)


    while True:
        cmd = prompt("输入命令 (按Tab补全): ", completer=command_completer)
        if cmd in cmds:
            cmds[cmd]()






"""

开始写起线程的代码了，我居然还有点紧张（？，有点好笑,难道是我是一口气写完的没有测试？/
万一报错了就不好了   不要报错出bug呐,佛祖保佑 25/8/3




成功了！！！哈哈，这套接字编程还挺简单的嘛，虽然还是修了点小bug，但也无伤大雅/
主要是这代码我是一口气写完的，没有调试，在写客户端的时候才调试的，哈哈哈哈/
太爽了，我现在真的很兴奋。虽然看起来很自恋，但是我还是想说下，太NB啦，哈哈哈哈 25/8/4

不行，实在是太兴奋了，写不下去了,容我在这发下牢骚。/
虽然这还是个半成品，但是，但是，这也是我写的第一个网络编程的东西/
我写的东西可以联网了！！里程碑，绝对，绝对是我人生的里程碑/
不行，现在才是个半成品就这么兴奋了，这写完还的了。我要去缓解下我兴奋的情绪了 25/8/4


昨天完成了退出检测，但是感觉不符合我的协议，为了适配不久就要写的通信广播功能，只能重构了下task函数/
但是出现了非常多细节上的bug（，好吧，我其实是偷懒了，没有重新写只是在现有的基础上将功能剥离出去/
最后函数调用时没有做好适配工作... 25/8/6


广播完成了，但是意外的不怎么激动？为什么呢  25/8/7

私聊功能也完成了，这个项目大体是完成了，后面有时间再优化下就可以了 /
说实话我还是想重构下的，这个项目是我边构思遍写的，可以说说是一开始就没有设计好 25/8/10

"""
