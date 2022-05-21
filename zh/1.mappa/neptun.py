# max 10 Elfogad, elutasit
from socket import *
from select import *
import sys
sock_srv = socket(AF_INET, SOCK_STREAM)
sock_srv.bind(('localhost', 10001))

#tanár
#sock_chs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock_chs.connect(('localhost', 10001))
sock_srv.listen()
sock_srv.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
socks = [sock_srv]

days = [1,8,15,22,29]
vizsgazok = [[],[],[],[],[]]

len(sys.argv)
while True:
    readable, _, _ = select(socks, [], [], 1)
    for active in readable:
        if active == sock_srv:
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
                msg_unpacked = msg.decode('UTF-8').split(' ')
                print(msg_unpacked)
                id = int(msg_unpacked[0])
                nap = int(msg_unpacked[1])
                reply = ""
                tarolt=0
                print(nap)
                finished = False
                while tarolt < len(days) and finished:
                    print(tarolt)
                    if days[tarolt] == nap:
                        finished=True
                    else:
                        ++tarolt
                print(tarolt)
                print(vizsgazok[tarolt])
                if len(vizsgazok[tarolt])==10:
                    reply = "ELUTASIT"
                else:
                    reply = "ELFOGAD"
                    vizsgazok[tarolt].append(id)
                print (vizsgazok)
                print(reply)
                active.sendall(reply.encode('utf-8'))



