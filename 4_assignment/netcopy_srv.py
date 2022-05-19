import socket
import sys
import zlib
import os

sock_srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_srv.bind((sys.argv[1], int(sys.argv[2])))

sock_chs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_chs.connect((sys.argv[3], int(sys.argv[4])))

fileId = sys.argv[5]
filePath = sys.argv[6]

sock_srv.listen()
finish = False

while not finish:
    cli, addr = sock_srv.accept()
    msg = cli.recv(1024)
    msg_unpacked = msg.decode('UTF-8')
    txt = ""
    while msg_unpacked != "EOF":
        txt = txt + msg_unpacked
        msg = cli.recv(1024)
        msg_unpacked = msg.decode('UTF-8')
    finish = True
    assert os.path.isfile(filePath)
    with open(filePath, "w") as f:
        f.write(txt)
    f.close
cli.close()

crc = hex(zlib.crc32((txt).encode('UTF-8')) % (1 << 32))
#print(crc)
#print(("KI|" + fileId).encode('UTF-8'))
sock_chs.sendall(("KI|" + fileId).encode('UTF-8'))
cs = sock_chs.recv(len(crc))
sock_chs.close()

cs_unpacked = str(cs.decode('UTF-8'))

result = ""
if (cs == crc):
    result = "CSUM OK"
else:
    result = "CSUM CORRUPTED"
print(result)