from socket import *
from select import *
import sys

srv = socket(AF_INET, SOCK_STREAM)
srv.bind((sys.argv[1], int(sys.argv[2])))
srv.listen()
srv.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
socks = [srv]

store = dict()

while True:
    readable, _, _ = select(socks, [], [], 1)
    for active in readable:
        if active == srv:
            cli, addr = active.accept()
            #print("New client ", addr)
            socks.append(cli)
        else:
            #print(active)
            msg = active.recv(1024)
            msg_unpacked = msg.decode('UTF-8')
            #print('sdakf' + msg_unpacked)
            header = msg_unpacked.split('|')[0]
            reply = ""
            if header == "BE":
                fileId = msg_unpacked.split('|')[1]
                validTime = msg_unpacked.split('|')[2]
                checksumLength = msg_unpacked.split('|')[3]
                checksum = msg_unpacked.split('|')[4]
               # print(fileId + validTime + checksumLength + checksumLength +checksum)
                store[fileId] = [checksum, validTime]
            elif header == "KI":     
                fileId = msg_unpacked.split('|')[1]
                reply = str(store[fileId][0]).encode('utf-8')
                #print(reply)
                cli.sendall(reply)
                del store[fileId]
