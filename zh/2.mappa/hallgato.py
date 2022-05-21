#azonosito generalas 100002 10100  [1,8,15,22,29]
#bytes formátum
import random
from select import select
from socket import *


days = [1,8,15,22,29]
with socket(AF_INET, SOCK_STREAM) as sock:
    sock.connect(('localhost', 10001))
    id = random.randint(10002 , 10100 )
    nap = days[random.randint(0,len(days))]
    sock.sendall((str(id) + ' ' + str(nap)).encode('UTF-8'))
    print("elküldtem")
    print(str(id) + str(nap))

    while True:
        reply = (sock.recv(2000).decode('UTF-8'))
        print(reply)
        if reply == "ELFOGAD":
            print("varunk")
            sock_srv = socket(AF_INET, SOCK_STREAM)
            sock_srv.bind(('localhost', id))
            sock_srv.listen()
            sock_srv.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            finished = True
            socks = [sock_srv]
            while not finished:
                readable, _, _ = select(socks, [], [], 1)
                for active in readable:
                    if active == sock_srv:
                        cli, addr = active.accept()
                        print("New client ", addr)
                        socks.append(cli)
                    else:
                        msg = active.recv(1000)
                        print(msg)
                        if not msg:
                            active.close()
                            socks.remove(active)
                            print("Client left")
                        else:
                            msg_unpacked = msg.decode('UTF-8')
                            print(msg_unpacked)
                            finished = False
        else:
            break;