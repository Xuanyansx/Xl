import selectors
import socket as sk

server = sk.socket()
server.bind(("127.0.0.1",51277))
server.listen(10)
server.setblocking(False)

def clinet(conn:sk.socket):
    try:
        data = conn.recv(1024)
        if not data:
            conn.close()
            sel.unregister(conn)
            return
        
        conn.send(data)
    except :
        conn.close()
        sel.unregister(conn)
        return


def acc(ser:sk.socket):
    print(ser is server)
    conn,addr = ser.accept()
    sel.register(conn,selectors.EVENT_READ,clinet)
    


sel = selectors.DefaultSelector()
sel.register(server,selectors.EVENT_READ,acc)


while True:
    rlist = sel.select()

    for key,en in rlist:
        func = key.data
        func(key.fileobj)
