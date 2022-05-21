#azonosito generalas 100002 10100  [1,8,15,22,29]
#bytes formátum
import random
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
        break;