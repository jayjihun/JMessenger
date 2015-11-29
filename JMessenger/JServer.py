from socketserver import TCPServer, StreamRequestHandler
from socket import *
from time import ctime, sleep
import sys
from queue import Queue
from threading import Thread
import re
from ServerDB import ServerDB

HOST = '175.198.72.181' #must be input parameter @TODO
PORT = 11557
ADDR = (HOST,PORT)
inputs = Queue()
sendsock = socket(AF_INET,SOCK_STREAM)
identifier = re.compile(r'[a-zA-Z0-9_]{4,12}')

class Message(object):
    def __init__(self,line,ip_from,wfile):
        self.line = line
        self.ip_from = ip_from
        self.wfile=wfile
        #self.wfile.write("Message()".encode())

class WorkerThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.db = None

    def jointry(self,line):
        id = line.split(' ')[1]
        pw = line.split(' ')[2]
        if identifier.fullmatch(id) is None:
            return 'JOINR FAIL INVALIDID'
        if identifier.fullmatch(pw) is None:
            return 'JOINR FAIL INVALIDPW'
        if self.db.joinuser(id,pw):
            return 'JOINR SUCCESS'
        return 'JOINR FAIL DUPLICATE'


    def execute(self,line,ip_from):
        try:
            code = line.split(' ')[0]
            if code == 'JOIN':
                return self.jointry(line)
        except:
            return 'NOT'
        return 'NOT'

    def send(self,reply,wfile):
        try:
            wfile.write(bytes(reply+"\n",'utf-8'))
        except Exception as e:
            print("Send failed")

    def run(self):
        self.db = ServerDB()
        print("Start Server")
        while True:
            message = inputs.get()
            reply = self.execute(message.line,message.ip_from)
            print(message.ip_from)
            print('Reply :',reply)
            self.send(reply,message.wfile)
    
class ServerHandler(StreamRequestHandler):
    def handle(self):
        add = self.client_address
        content = self.rfile.readline().strip().decode('utf-8')
        message = Message(content,add,self.wfile)
        sleep(2)
        self.
        self.wfile.write("Got it".encode())
        inputs.put(message)
        
        print("IP : %s, Message : %s"%(add,content))



def main():
    tcpServ = TCPServer(ADDR, ServerHandler)
    wthread = WorkerThread()
    wthread.start()
    tcpServ.serve_forever();

if __name__ == '__main__':
    main()