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


loggedin = False

def send(addr, message):
    soc = socket(AF_INET, SOCK_STREAM)
    soc.connect(addr)
    soc.send(bytes(message+"\n",'utf-8'))
    soc.close()

def poke(addr,message):
    soc = socket(AF_INET, SOCK_STREAM)
    soc.connect(addr)
    soc.send(bytes(message+"\n",'utf-8'))
    rcv = soc.recv(BUFSIZE).decode('utf-8')
    soc.close()
    return rcv

class ListenThread(Thread):
    def __main__(self):
        Thread.__init__(self)
        self.port = 0

    def serve(self,line):
        print("RECEIVED :",line)

    def listen(self):
        soc = socket(AF_INET, SOCK_STREAM)
        soc.bind(('',self.port))
        soc.listen()
        while True:
            acc,add = soc.accept()
            rcv = acc.recv(BUFSIZE).decode('utf-8')
            self.serve(rcv)
            acc.close()

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
            message = "LOGIN %s %s"%(id,pw)
            

            soc = socket(AF_INET, SOCK_STREAM)
            soc.connect(SERVER)
            soc.send(bytes(message+"\n","utf-8"))
            rcv = soc.recv(BUFSIZE).decode('utf-8')
            port = soc.getsockname()[1]
            soc.close()
            
            try:
                op,code = rcv.split(' ')[0],rcv.split(' ')[1]
            except Exception as e:
                print(e.args)
                print("UNKNOWN ERROR1")
                continue
            if op != 'LOGINR':
                print("UNKNOWN ERROR2")
                continue
            if code != 'SUCCESS':
                print("Log in failed :", rcv.split(' ')[-1])
                continue
            print("Log in success.")
            self.port = port
            global loggedin
            loggedin = True
            break

    def run(self):

        self.login()
        self.listen()

            

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
        break
       
listener = ListenThread()
listener.start()
while not loggedin:
    pass        

while True:
    op = input("Select Menu : 1. Chat, 2. Log out > ")
    if op=='1':
        otherid = input("Select his ID > ")
        message = "CON %s"%(otherid,)
        rcv = poke(SERVER,message)
        try:
            op,code = tuple(rcv.split(' ')[0:2])
        except Exception as e:
            print(e.args)
            print("UNKNOWN ERROR1")
            continue
        if op != 'CONR':
            print("UNKNOWN ERROR2")
            continue
        if code == 'SUCCESS':
            print("Con info received.")
            info = ' '.join(rcv.split(' ')[2:])
            addr = (info.split(' ')[0],int(info.split(' ')[1]))
            print('Info :',info)
            for i in range(1,5):
                send(addr,'HI YOU ALRIGHT?')
                sleep(3)
            continue
        else:
            print("Con Failed :",rcv.split(' ')[-1])
            continue

    elif op=='2':
        pass
