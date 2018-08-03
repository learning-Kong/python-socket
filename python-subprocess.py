# -*- coding: utf-8 -*-

import subprocess

# 命令执行正确
obj = subprocess.Popen('ipconfig',shell=True,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
print(obj)
print( 'studout:', obj.stdout.read().decode('gbk'))     # windows解码成gbk  # 并且只能从管道读一次
print('studerr:', obj.stderr.read().decode('gbk'))      # linux解码成utf-8


# 命令执行错误
obj = subprocess.Popen('dissr', shell=True,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       )

print(obj)
print('studout:', obj.stdout.read().decode('gbk')) # windows解码成gbk
print('studerr:', obj.stderr.read().decode('gbk'))   # linux解码成utf-8
