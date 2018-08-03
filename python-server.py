# -*- coding: utf-8 -*-

import socket

phone = socket.socket(socket.AF_INET,socket.SOCK_STREAM)        #设置ipv4和端口协议为TCP

phone.bind(('127.0.0.1',9992))    #port:0-65535 (0-1024给os使用)     #绑定主机和端口

phone.listen(5)     #开始TCP监听，开始后等待连接，最多接受5个客户端

while True:
    print ('i am watting ......')
    conn,client_addr = phone.accept()   #被动接受TCP客户的连接,(阻塞式)等待连接的到来
    print (conn)
    print (client_addr)

    while True:
        try:
            data = conn.recv(1024)      #1.单位是： bytes     2.1024代表最大接受1024bytes
            print ('recv client massage: ', data.decode('utf-8'))

            conn.send(data.upper())     # 转换为大写诶，发送过去
        except Exception as e:
            print ('error info is： ',e)
            break
    conn.close()            #关闭套接字

phone.close()           #关闭连接
