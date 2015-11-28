from socketserver import (TCPServer as TCP, StreamRequestHandler as SRH)
from socket import *
from time import ctime, sleep
import sys
from queue import Queue
from threading import Thread
import re
from ServerDB import ServerDB

HOST = '175.198.72.171'
PORT = 11557
ADDR = (HOST,PORT)
inputs = Queue()
sendsock = socket(AF_INET,SOCK_STREAM)
identifier = re.compile(r'[a-zA-Z0-9_]{4,12}')

class Message(object):
    def __init__(self,line,ip_from):
        self.line = line
        self.ip_from = ip_from

class WorkerThread(Thread):
    def __init__(self):
        Thread.__init__(self)
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
            print(code)
            if code == 'JOIN':
                return self.jointry(line)
        except:
            return 'NOT'
        return 'hi'

    def run(self):
        self.db = ServerDB()
        while True:
            while not inputs.empty():
                message = inputs.get()
                line = message.line
                ip_from = message.ip_from
                reply = self.execute(line,ip_from)
                print('Reply :',reply)
                sendsock.connect(ip_from)
                sendsock.send(bytes(reply,'utf-8'))
                sendsock.close()
    
class ServerHandler(SRH):
    def handle(self):
        add = self.client_address
        content = self.rfile.readline().strip().decode('utf-8')
        message = Message(content,add)
        inputs.put(message)
        print("IP : %s, Message : %s"%(add,content))



def main():
    tcpServ = TCP(ADDR, ServerHandler)
    wthread = WorkerThread()
    wthread.start()
    tcpServ.serve_forever();

if __name__ == '__main__':
    main()