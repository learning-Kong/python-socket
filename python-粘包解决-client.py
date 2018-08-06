# -*- coding:utf-8 -*-
#author: "Xianglei Kong"

import struct
import socket
import json

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(('127.0.0.1',9995))

while True:

    data = input('>>>>').strip()    # 粘包现象，当输入ipconfig的时候，缓存池会存放太多的结果
    if not data:
        continue
    client.send(data.encode('utf-8'))

    # 2.接受报头的长度         4 个bytes----》struct----》 header_bytes的len
    header_size_rev = client.recv(1024)
    header_size_len = struct.unpack('i',header_size_rev)[0]

    #3.接受json数据

    header_json_rev = client.recv(header_size_len)
    print(header_json_rev)

    #3.2 解析json数据
    header_json = header_json_rev.decode('utf-8')
    header_dict = json.loads(header_json)

    #接收server端数据
    total_data = b''
    recv_size = 0

    while recv_size < header_dict['total_size']:     # 接受的数据长度 = len（total_data） 已经取完了，就退出
        print (1)
        data = client.recv(1024)
        recv_size += len(data)
        total_data += data
    print(total_data.decode('gbk'))
client.close()