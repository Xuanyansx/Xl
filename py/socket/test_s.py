import socket as sk

server = sk.socket()
server.bind(("127.0.0.1",51277))
server.listen(10)
conn,addr = server.accept()



msg = b''
while True:
    data_size = conn.recv(4).decode("utf-8")
    data_size = int(data_size)
    while True:
        # if data_size<=0:
        #     break

        data_size-=2
        data = conn.recv(2)
        msg+=data
        print(data,msg,data_size)
        if data_size<0:
            break

    # print(msg,"\n\n")

