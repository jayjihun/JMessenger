from socket import *
import sys
from time import sleep
import re
from threading import Thread

SERIP = "175.198.72.181"
SERPORT = 11557;
BUFSIZE = 1024
SERVER = (SERIP,SERPORT);
keepgoing = True
identifier = re.compile(r'[a-zA-Z0-9_]{4,12}')

PORT = 22557

loggedin = False

class ListenThread(Thread):
    def __main__(self):
        pass

    def login(self):
        while True:
            id = input("Type ID > ")
            pw = input("Type PW > ")
            if identifier.fullmatch(id) is None:
                print("Invalid ID")
                continue
            if identifier.fullmatch(pw) is None:
                print("Invalid PW")
                continue



while True:
    op = input("Select Menu : 1. Join, 2. Login > ")
    if op == "1": #Join
        newid = input("Type new ID > ")
        newpw = input("Type new PW > ")
        if identifier.fullmatch(newid) is None:
            print("Invalid ID")
            continue
        if identifier.fullmatch(newpw) is None:
            print("Invalid PW")
            continue
        soc = socket(AF_INET, SOCK_STREAM)
        message = "JOIN %s %s"%(newid, newpw)
        soc.connect(SERVER)
        soc.send(bytes(message+"\n",'utf-8'))
        rcv = soc.recv(BUFSIZE).decode('utf-8')
        soc.close()

        try:
            op,code = rcv.split(' ')[0],rcv.split(' ')[1]
        except Exception as e:
            print(e.args)
            print("UNKNOWN ERROR1")
            continue
        if op != 'JOINR':
            print("UNKNOWN ERROR2")
            continue
        if code == 'SUCCESS':
            print("Join success.")
            continue
        else:
            print("Join Failed :",rcv.split(' ')[-1])
            continue
            
    elif op == "2":#Login
        listener = ListenThread()
        listener.start()
        while loggedin:
            pass
        
