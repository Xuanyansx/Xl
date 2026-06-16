


import socket as sk
import select




server = sk.socket()
server.bind(("127.0.0.1",51277))
server.listen(10)
server.setblocking(False)
ilist = [server]

while True:
    print("wwew")
    rlist,wlist,xlist = select.select(ilist,[],[])
    print(rlist)
    for i in rlist:
        print(rlist)

        if i is server:
            conn,addr = i.accept()
            ilist.append(conn)
            print(ilist)
            continue
        
        try:
            data = i.recv(1024)
            if not data:
                i.close()
                ilist.remove(i)
                continue
            i.send(data)
        except :
            i.close()
            ilist.remove(i)
            continue

