import random
from socket import *
from select import *
import sys
import struct

n = random.randint(1, 100)
print("Kitalálandó szám")
print(n)
srv = socket(AF_INET, SOCK_STREAM)
srv.bind((sys.argv[1], int(sys.argv[2])))
#srv.bind(('localhost', 10000))
srv.listen()
srv.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
finished = False
socks = [srv]

while not finished:
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
                unpacked_msg = struct.Struct("1s I").unpack(msg);
                guess_signal = (str(unpacked_msg[0]))[2]
                guess_number = int(unpacked_msg[1])
                reply = ""
                if guess_number == n and guess_signal == '=':
                    reply = 'Y'
                    for s in socks:
                        if s != active and s != srv:
                            msg = ('V'.encode('utf-8'), 0)
                            s.sendall(struct.Struct("1s I").pack(*msg))
                    finished = True
                elif guess_signal == '=':
                    reply = 'K'
                    socks.remove(active)
                elif (guess_signal == '>' and guess_number < n) or (guess_signal == '<' and guess_number > n):
                    reply = 'I'
                else:
                    reply = 'N'
                print(guess_number )
                print(guess_signal)
                print("Válasz " + reply )
                msg = (reply.encode('utf-8'), 0)
                active.sendall(struct.Struct("1s I").pack(*msg))

