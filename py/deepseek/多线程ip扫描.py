import socket as sk
from threading import Thread


def test(ip):
    c = sk.socket()

    for i in range(1145):
        try:
            c.connect((ip,i))
            print(f"连接成功{ip} {i}")
        except:
            pass



p = Thread(target=test)
p.start()
        