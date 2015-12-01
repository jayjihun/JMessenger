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
    def __init__(self):
        Thread.__init__(self)
        self.loggedin = False        
        self.port = 0
        self.keepgoing = True
        self.id=None
        self.pw=None

    def send(self,addr, message):
        soc = socket(AF_INET, SOCK_STREAM)
        soc.connect(addr)
        soc.send(bytes(message+"\n",'utf-8'))
        print("[LISTENER] Send :",message)
        soc.close()

    def poke(self, addr,message):
        soc = socket(AF_INET, SOCK_STREAM)
        soc.connect(addr)
        soc.send(bytes(message+"\n",'utf-8'))
        print("[LISTENER] Send :",message)
        rcv = soc.recv(BUFSIZE).decode('utf-8')
        print("[LISTENER] Received :",rcv)
        soc.close()
        return rcv

    def dummy(self,line):
        print('DUMMY received')
        pass

    def througher(self,line):
        try:
            print(1)
            ip = line.split(' ')[2]
            print(2)
            port = int(line.split(' ')[3])
            print(3)
            addr = (ip,port)
            print(4)
            print(addr)
            send(addr,'THRU HELLO')
            print(5)
        except Exception as e:
            print("Error detected!!")
            print(e.args)


    def process(self,line):
        funcs={'CONR':self.througher,'THRU':self.dummy}
        try:
            code = line.split(' ')[0]
            funcs[code](line)
        except KeyError:
            pass
        except Exception as e:
            print(e.args)
            pass

    def listen(self):
        soc = socket(AF_INET, SOCK_STREAM)
        print("Start Listening. Port :",self.port)
        soc.bind(('',self.port))
        soc.listen()
        while keepgoing:
            acc,add = soc.accept()
            rcv = acc.recv(BUFSIZE).decode('utf-8')
            print('RECEIVED :',rcv)
            self.process(rcv)
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
            self.id=id
            self.pw=pw
            self.loggedin = True
            break

    def run(self):
        self.login()
        self.listen()

    def getid(self):
        if not self.loggedin:
            return None
        else:
            return (self.id,self.pw)

class Client(object):
    def __init__(self):
        self.id=None
        self.pw=None
        pass

    def send(self,addr, message):
        soc = socket(AF_INET, SOCK_STREAM)
        soc.connect(addr)
        soc.send(bytes(message+"\n",'utf-8'))
        print("[CLIENT] Send :",message)
        soc.close()

    def poke(self, addr,message):
        soc = socket(AF_INET, SOCK_STREAM)
        soc.connect(addr)
        soc.send(bytes(message+"\n",'utf-8'))
        print("[CLIENT] Send :",message)
        rcv = soc.recv(BUFSIZE).decode('utf-8')
        print("[CLIENT] Received :",rcv)
        soc.close()
        return rcv

    def greet(self):
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
                message = "JOIN %s %s"%(newid, newpw)
                rcv = self.poke(SERVER, message)
                op,code = rcv.split(' ')[0],rcv.split(' ')[1]
                # try:                    
                '''
                except Exception as e:
                    print(e.args)
                    print("UNKNOWN ERROR1")
                    continue
                if op != 'JOINR':
                    print("UNKNOWN ERROR2")
                    continue
                    '''
                if code == 'SUCCESS':
                    print("Join success.")
                    continue
                else:
                    print("Join Failed :",rcv.split(' ')[-1])
                    continue
            
            elif op == "2":#Login
                break

    def memberaction(self):
        while True:
            op = input("Select Menu : 1. Chat, 2. Logout > ")
            if op=='1':
                otherid = input("Select his ID > ")
                message = "CON %s %s"%(self.id, otherid)
                rcv = self.poke(SERVER,message)
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
                    info = ' '.join(rcv.split(' ')[2:])
                    dstaddr = (info.split(' ')[0],int(info.split(' ')[1]))
                    print('Info :',info)
                    self.send(dstaddr,'THRU HELLO')
                    self.send(dstaddr,'MES This is real message. Hello.')
                    continue
                else:
                    print("Con Failed :",rcv.split(' ')[-1])
                    continue

            elif op=='2':
                break

    def start(self):
        self.greet()
        self.listener = ListenThread()
        self.listener.start()

        while True:
            a = self.listener.getid()
            if a is not None:
                self.id,self.pw=a
                break
        self.memberaction()


client = Client()
client.start()