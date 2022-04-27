import socket
import sys
import zlib

sock_srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_srv.connect((sys.argv[1], int(sys.argv[2])))

sock_chs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_chs.connect((sys.argv[3], int(sys.argv[4])))

fileId = sys.argv[5]
filePath = sys.argv[6]

txt = ""
with open(filePath, 'r') as f:
    for line in f:
        txt = txt + line
f.close()

crc = hex(zlib.crc32((txt).encode('UTF-8')) % (1 << 32))
reply = "BE|" + str(fileId) + "|60|" + str(len(crc)) + "|" + str(crc)

sock_chs.sendall(reply.encode('UTF-8'))
sock_chs.close()

with open(filePath, 'r') as f:
    for line in f:
        sock_srv.sendall(line.encode('UTF-8'))
    else:
        sock_srv.sendall("EOF".encode('UTF-8'))
        sock_srv.close
