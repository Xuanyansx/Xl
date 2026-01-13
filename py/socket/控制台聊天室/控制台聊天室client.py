import os
import socket as sk
from prompt_toolkit import prompt
from threading import Thread,Event
from prompt_toolkit.completion import WordCompleter



online = []
names = []
is_true = True
chat_ready = Event()
broadcast_event = Event()

def user_info():
    while True:
        global cname
        name = input("\n请输入用户名: ").strip()
        
        
        if not name:
            print("错误：用户名不能为空")
            continue
        if len(name) < 3:
            print("错误：用户名长度需至少3个字符")
            continue
        
        if len(name.encode('utf-8')) > 21:
            print("错误：用户名长度不能超过21字节")
            continue
        if not name.isalnum():
            print("错误：用户名只能包含字母和数字")
            continue
        
        passwd = input("请输入密码: ").strip()
        
        if not passwd:
            print("错误：密码不能为空")
            continue
        if len(passwd) < 8:
            print("错误：密码长度需至少8个字符")
            continue
        # 保持字节长度检查不变
        if len(passwd.encode('utf-8')) > 16:
            print("错误：密码长度不能超过16字节")
            continue
        
        has_upper = any(c.isupper() for c in passwd)
        has_lower = any(c.islower() for c in passwd)
        has_digit = any(c.isdigit() for c in passwd)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in passwd)
        
        if not (has_upper and has_lower and has_digit and has_special):
            print("错误：密码必须包含大写字母、小写字母、数字和特殊字符")
            continue
        cname = name
        return [name, passwd]
    


def recv_data(client,var_num=1):
    global is_true
    res = []

    for i in range(var_num):

        try:
            code = client.recv(4)
            data = client.recv(4)
        except Exception as e:
            is_true = False
            print("服务器好像亖了，回车下试试")
            # if e == "ConnectionAbortedError":
            return False
        if not data:
            is_true = False
            print("服务器好像亖了，回车下试试")
            return False
        msg_size = int(data.decode('utf-8'))
        
        msg = client.recv(msg_size)
        res.append(msg) 
    # print(code,*res,sep='\n')
    return code,*res

def user_send(client,msg):
    msg_bytes = msg.encode('utf-8')
    msg_size = len(msg_bytes)
    msg_head = bytes(str(msg_size),'utf-8').zfill(4)
    # print(msg_bytes,msg_head,msg_size)
    client.send(msg_head)
    client.send(msg_bytes)


def handle_code(client):
    global online
    global names

    while True:
        data = recv_data(client)

        if not data:
            print("break")
            break
        code = data[0].decode('utf-8') # type: ignore
        msg = data[1].decode('utf-8') # type: ignore

        if code == '0007':
            name,passwd = user_info()
            user_send(client,name)
            user_send(client,passwd)
            print("请求用户信息，如果没出现收集提示，请回车试试")
        if code == '0000':
            print("您还未注册，正在帮您注册")
        if code == '0001': 
            print("名称已被占用")
        if code == '0005':
            print("注册成功！")
        if code == '0008':
            print("请重新登录")
        if code == '0002':
            print("没有该用户")
        if code == '0003':
            print("密码错误")
        if code == '0004':
            print("验证失败，请重试")
        if code == '0006':
            print("登录成功")
        if code == '0009':
            print("可以通信了")
            chat_ready.set()
        if code == '0010':
            print(msg) 
        if code == '0011':
            print(msg)
        if code == '0012':
            # print(msg)
            # print(type(msg))
            online = eval(msg)
            names = [f"@{i}$ " for i in online]
            # print(type(online))
            # print(online)
        if code == '0013':
            print("私聊消息发送成功")
        if code == '0014':
            print("私聊消息发送失败")
            
        #什么？这里可以优化？这样写不优雅？笑死，我当然知道，只是暂时不想改罢了（懒 25/8/5



if __name__ == "__main__":
    client = sk.socket()
    while True:
        addr = input("输入ip地址")
        port = input("输入端口")

        try:
            client.connect((addr,int(port)))
        except Exception as e:
            print(e)
            print("\n连接失败，可能原因：\n1. IP/端口配置错误\n2. 服务器未运行\n3. 网络故障\n请逐项排查")
            continue


        print("欢迎来到聊天室，如果没有注册系统会自动帮你注册的")
        code_thread = Thread(target=handle_code,args=(client,))
        code_thread.daemon = True
        code_thread.start()

        cmds = {
            "exit":lambda : os._exit(0),
            "list":lambda : print("当前在线玩家有",*(i for i in online),sep='\n'),
            "help":lambda : print("私信消息 @<name> <消息> \nexit 退出 \n list 查看在线玩家")
        }

        while is_true:
            chat_ready.wait()
            command_completer = WordCompleter(list(cmds.keys())+names, ignore_case=True)
            chat = prompt(completer=command_completer)
            if chat in cmds:
                cmds[chat]()
                continue
            if not chat=="":
                user_send(client,chat)
        else :
            print("服务器连接异常,客户端退出\n")
            client.close()
            online = []
            names = []
            is_true = True
            chat_ready = Event()
            broadcast_event = Event()
            client = sk.socket()

    # client = sk.socket()
    # client.connect(('127.0.0.1',5277))

    # print("欢迎来到聊天室，如果没有注册系统会自动帮你注册的")
    # code_thread = Thread(target=handle_code,args=(client,))
    # code_thread.daemon = True
    # code_thread.start()


    # while True:
    #     chat_ready.wait()
    #     chat = input()
    #     if not chat=="":
    #         user_send(client,chat)
    
    # client.close()
