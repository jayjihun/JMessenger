from socketserver import TCPServer, StreamRequestHandler
from socket import *
from time import ctime, sleep
import sys
from queue import Queue
from threading import Thread
import re
from ServerDB import ServerDB

HOST = '175.198.72.181'
PORT = 11557
ADDR = (HOST,PORT)
inputs = Queue()
identifier = re.compile(r'[a-zA-Z0-9_]{4,12}')
db=ServerDB()

def send(addr, message: str):
    soc = socket()
    soc.connect(addr)
    soc.send(bytes(message,'utf-8'))
    soc.close()


    
class ServerHandler(StreamRequestHandler):

    def jointry(self,line,add):
        try:
            id = line.split(' ')[1]
            pw = line.split(' ')[2]
        except:
            return 'JOINR FAIL INVAL'
        if identifier.fullmatch(id) is None:
            return 'JOINR FAIL INVALIDID'
        if identifier.fullmatch(pw) is None:
            return 'JOINR FAIL INVALIDPW'
        if db.joinuser(id,pw):
            return 'JOINR SUCCESS'
        return 'JOINR FAIL DUPLICATE'

    def login(self,line,add):
        try:
            id = line.split(' ')[1]
            pw = line.split(' ')[2]
        except:
            return 'LOGINR FAIL INVAL'
        if identifier.fullmatch(id) is None:
            return 'LOGINR FAIL INVALIDID'
        if identifier.fullmatch(pw) is None:
            return 'LOGINR FAIL INVALIDPW'
        print("Set debug to",add)
        return db.loginuser(id,pw,add)

    def contry(self,line,add):
        try:
            srcid,dstid = tuple(line.split(' ')[1:3])
        except:
            return 'CONR FAIL INVAL'           
        if identifier.fullmatch(dstid) is None:
            return 'CONR FAIL INVALIDID'
        dstadd = db.conuser(dstid)
        if type(dstadd) == str:
            return dstadd
        srcadd = db.conuser(srcid)
        message2 = 'CONR SUCCESS %s %d'%srcadd
        send(dstadd,message2)
        return 'CONR SUCCESS %s %d'%dstadd

    def logout(self,line,add):
        try:
            id = line.split(' ')[1]
        except:
            return 'LOGOUTR FAIL'
        if identifier.fullmatch(id) is None:
            return 'LOGOUTR FAIL INVALIDID'
        return db.logoutuser(id)

    def process(self, line, add):
        funcs = {'JOIN':self.jointry, 'LOGIN':self.login, 'CON':self.contry, 'LOGOUT':self.logout}
        try:
            code = line.split(' ')[0]
            return funcs[code](line,add)
        except Exception as e:
            print(e.args)
        return 'NOT'


    def handle(self):
        print("[REQUEST arrived]")
        add = self.client_address
        content = self.rfile.readline().strip().decode('utf-8')
        print("IP : %s, Message : %s"%(add,content))
        reply = self.process(content, add)
        print("Reply :",reply)
        self.wfile.write(bytes(reply,'utf-8'))

def main():
    print("Start Server")
    tcpServ = TCPServer(ADDR, ServerHandler)
    
    tcpServ.serve_forever();

if __name__ == '__main__':
    main()