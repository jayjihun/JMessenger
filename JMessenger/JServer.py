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
sendsock = socket(AF_INET,SOCK_STREAM)
identifier = re.compile(r'[a-zA-Z0-9_]{4,12}')
db=ServerDB()

    
class ServerHandler(StreamRequestHandler):
    def jointry(self,line):
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
            otherid = line.split(' ')[1]
        except:
            return 'CONR FAIL INVAL'           
        if identifier.fullmatch(otherid) is None:
            return 'CONR FAIL INVALIDID'
        otheradd = db.conuser(otherid)
        if type(otheradd) == str:
            return otheradd
        return 'CONR SUCCESS %s %d'%otheradd

    def logout(self,line):
        try:
            id = line.split(' ')[1]
        except:
            return 'LOGOUTR FAIL'
        if identifier.fullmatch(id) is None:
            return 'LGOUTR FAIL INVALIDID'
        return db.logoutuser(id)

    def process(self, line, add):
        try:
            code = line.split(' ')[0]
            if code == 'JOIN':
                return self.jointry(line)
            elif code == 'LOGIN':
                return self.login(line,add)
            elif code == 'CON':
                return self.contry(line,add)
            elif code == 'LOGOUT':
                return self.logout(line)
        except Exception as e:
            print(e.args)
            return 'NOT'
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