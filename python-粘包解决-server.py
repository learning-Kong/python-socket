# -*- coding: utf-8 -*-
#author: "Xianglei Kong"


import struct
import socket
import subprocess
import json

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind(('127.0.0.1',9994))

server.listen(5)

while True:
    print (">>:")
    conn,addr = server.accept()
    while True:
        try:
            data = conn.recv(1024)
            print('=>',data)
            if not data:
                break
            obj = subprocess.Popen(data.decode('utf-8'),shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
            # 获得命令结果
            stdout = obj.stdout.read()
            stderr = obj.stderr.read()
            #将数据编辑制作
            #1 制作报头
            total_size = len(stdout + stderr)
            header_dict = {
                'filename':'a.txt',
                'md5':'234easdasdad',
                'total_size': total_size
            }
            header_json = json.dumps(header_dict)   #将报头编码
            header_bytes = header_json.encode('utf-8')  # 报头---报头.json---报头.bytes

            #2 发送报头长度
            header_len  = struct.pack('i',len(header_bytes))     # 报头bytes---> len()---> struct
            conn.send(header_len)

            #3 把报头发送给客户端
            conn.send(header_bytes)

            #4 把真实数据发送给客户端
            conn.send(stdout)
            conn.send(stderr)
        except Exception as e:
            print (e)
            break
    conn.close()

server.close()