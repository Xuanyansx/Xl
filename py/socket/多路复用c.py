import socket as sk
from threading import Thread


def client(i):
    c = sk.socket()
    c.connect(("127.0.0.1",51277))
    while True:
        c.send(f"{i}".encode("utf-8"))
        data = c.recv(1024)
        print(data)
    


if __name__ == "__main__":
    for i in range(10):
        c = Thread(target=client,args=(i,))
        c.start()

