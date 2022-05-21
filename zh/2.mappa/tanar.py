import sys
import random
from select import select
from socket import *

srv = socket(AF_INET, SOCK_STREAM)
srv.bind(('localhost', 10003))
srv.listen()
srv.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
socks = [srv]

while True:
    readable, _, _ = select(socks, [], [], 1)
    for active in readable:
        if active == srv:
            cli, addr = active.accept()
            print("New client ", addr)
            socks.append(cli)
        else:
            msg = active.recv(1000)
            if not msg:
                active.close()
                socks.remove(active)
                print("Client left")
            else:
                msg_unpacked = msg.decode('UTF-8')
                print(msg_unpacked)
                id = int(msg_unpacked)
                n = random.randint(1, 5)
                with socket(AF_INET, SOCK_STREAM) as sock:
                    sock.connect(('localhost', id))
                    sock.sendall((str(n)).encode('UTF-8'))
