# -*- coding:utf-8 -*-

import socket
import subprocess

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind(('127.0.0.1',9998))

server.listen(5)

while True:
    print ('I am watting.....')
    conn,addr = server.accept()
    print ('client info:',addr)
    while True:
        msg = conn.recv(1024)
        if len(msg) == 0: break
        res = subprocess.Popen(msg.decode('utf-8'),shell=True,
                               stdout = subprocess.PIPE,
                               stdin = subprocess.PIPE,
                               stderr = subprocess.PIPE)
        stderr = res.stderr.read()
        stdout = res.stdout.read()
        print (msg.decode('utf-8'))
        print("res length",len(stdout))
        print (stdout.decode('gbk'))
        print (res.stdin)
        print (res.stdout)
        print (res.stderr)
        conn.send(stderr)
        conn.send(stdout)
    conn.close()