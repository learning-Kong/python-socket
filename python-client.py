# -*- coding: utf-8 -*-

import socket

phone = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

phone.connect(('127.0.0.1',9992))
while True:
    data = input('>>: ').strip()
    phone.send(data.encode('utf-8'))
    data = phone.recv(1024)
    print ('server recv massage: ', data.decode('utf-8'))

phone.close()