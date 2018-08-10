# -*- conding:utf-8 -*-
#author: 'Xianglei Kong'

import socket
import struct
import os
import json
import hashlib

def get (comds,conn):
    filename = comds.decode('utf-8').split()[1] # 获取basename

    #绝对路径的拼接
    SERVER_PATH = os.path.dirname(os.path.abspath(__file__))
    FILE_PATH = os.path.join(os.path.join(SERVER_PATH,'share'),filename)
    print (FILE_PATH)

    #以读的方式将文件中的数据传送给客户端

    #1. 制作报头
    header_dict = {
        'filename':filename,
        'total_size': os.path.getsize(FILE_PATH)
    }
    header_json = json.dumps(header_dict)   #将报头转换成json
    header_bytes = header_json.encode('utf-8')#报头------->报头.json ---------->报头.bytes

    #发送报头长度
    header_len = struct.pack('i',len(header_bytes)) #报头.bytes--->len()------>struct
    conn.send(header_len)

    #2 发送真实表头数据
    conn.send(header_bytes)

    #3 发送真实数据,并验证MD5
    with open(FILE_PATH,'rb') as f:
        m = hashlib.md5()
        for line in f:
            m.update(line)
            conn.send(line)

    #发送文件的md5
    conn.send(m.hexdigest().encode('utf-8'))

def main():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(('127.0.0.1',1995))
    server.listen(5)
    while True:
        print ('I am wating.......')
        conn,addr = server.accept()
        while True:
            try:
                comds = conn.recv(1024)
                print ('=>',comds)
                if not comds:
                    break
                com_type = comds.decode('utf-8').split()[0]
                if com_type == 'get':
                    get(comds,conn)
                # if com_type == 'put':
                #     put(conn)
            except Exception as e:
                print (e)
                break
        conn.close()
    server.close()

if __name__ == '__main__':
    main()