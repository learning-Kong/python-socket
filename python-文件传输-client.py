# -*- coding: utf-8 -*-
# author: "Xianglei Kong"

import os
import json
import struct
import socket
import hashlib

def get(client):

    # 接受报头的长度
    header_struct_len = client.recv(1024)
    header_bytes_len = struct.unpack('i',header_struct_len)[0]
    print (header_bytes_len)

    #接受报头json
    header_json = client.recv(header_bytes_len)
    header_dict = json.loads(header_json.decode('utf-8'))

    total_size = header_dict['total_size']
    filename = header_dict['filename']

    #打开文件，写入内容，文件路径修改
    CLIENT_PATH = os.path.dirname(os.path.abspath(__file__))
    FILE_PATH = os.path.join(os.path.join(CLIENT_PATH,'download'),filename)

    m = hashlib.md5()
    with open(FILE_PATH,'wb') as f:
        recv_size = 0
        while recv_size < total_size:
            if total_size - recv_size > 1024:
                data = client.recv(1024)
            else:
                data = client.recv(total_size - recv_size)
            m.update(data)
            f.write(data)
            recv_size += len(data)
            print("总共%s bytes 已经传输%s bytes" % (total_size, recv_size))  # 简易进度条
        else:
            new_file_md5 = m.hexdigest()
            recv_file_md5 = client.recv(1024)
            print (1)
            if new_file_md5 == recv_file_md5.decode('utf-8'):
                print ('\033[31;2m recv success\033[0m')

def main():
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(('127.0.0.1',1995))

    while True:
        cmds = input('>>: ').strip()
        if not cmds:
            continue
        client.send(cmds.encode('utf-8'))
        com_type = cmds.split()[0]
        if com_type == 'get':
            get(client)
    client.close()
if __name__ == '__main__':
    main()