import struct
import socket
import sys
from math import ceil

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((sys.argv[1], int(sys.argv[2])))
    #sock.connect(('localhost', 10000))
    min = 0
    max = 100
    guess_sign = '<'
    guess_number = 50
    msg = (guess_sign.encode('utf-8'), guess_number)
    guess = struct.Struct("1s I").pack(*msg)
    sock.sendall(guess)

    while True:
        reply = (str(struct.Struct("1s I").unpack(sock.recv(2000))[0]))[2]
        print(reply)
        if reply == 'V' or reply == 'Y':
            break;
        if reply == 'N':
            if guess_sign == '<' and min != guess_number:
                guess_sign = '>'
                min = guess_number
            elif guess_sign == '>' and max != guess_number:
                guess_sign = '<'
                max = guess_number
            else:
                guess_sign = '='
        if reply == 'I':
            if guess_sign == '<':
                max = guess_number
            elif guess_sign == '>':
                min = guess_number
            guess_number = int(min + ceil((max-min)/2))

        print(guess_sign)

        print(guess_number)
        msg = (guess_sign.encode('utf-8'), guess_number)
        guess = struct.Struct("1s I").pack(*msg)
        sock.sendall(guess)

    sock.close()
