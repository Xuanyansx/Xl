import socket as sk


clinet = sk.socket()
clinet.connect(("127.0.0.1",51277))

while True:
    msg = input(">>>>").encode("utf-8")
    msg_size = len(msg)

    msg_head = bytes(str(msg_size),'utf-8').zfill(4)

    print(msg_size)
    print(msg_head)
    clinet.send(msg_head)
    clinet.send(msg)