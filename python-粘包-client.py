# -*- coding:utf-8 -*-

import socket
import subprocess

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(('127.0.0.1',9998))

while True:
    msg = input('>>:').strip()
    if len(msg) == 0: continue
    if msg == 'quit':break

    client.send(msg.encode('utf-8'))
    client_res = client.recv(1024)
    print (client_res.decode('gbk'),end='')