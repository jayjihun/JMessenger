from socket import *
import sys
from time import sleep

HOST = "175.198.72.181"
PORT = 11557;
BUFSIZE = 1024
ADDR = (HOST,PORT);
keepgoing = True


while True:
    sys.stdout.flush();
    tcpCliSock = socket(AF_INET,SOCK_STREAM);
    
    data = input(">");
    if not data:
        break;
    tcpCliSock.connect(ADDR);
    tcpCliSock.send(bytes(data+"\n","utf-8"));
    rcv = tcpCliSock.recv(BUFSIZE)    
    if rcv:
        print(rcv.decode('utf-8'))