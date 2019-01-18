#!/usr/bin/python
#-*- coding: utf-8 -*-

import socket
import time
import os
import platform


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('169.254.1.30', 7610))
buf = []
len_log = 0
interval_time = 0
cur_dir = os.getcwd()
spit = '/'
file_name = 'log.txt'
if 'Windows' == platform.system():
    spit = '\\'
log_file_path = cur_dir + spit + file_name
with open(log_file_path, 'wb') as f:
    while True:
        buf = s.recv(1024)
        if 0 == len_log:
            start = time.time()
        if buf:
            len_log += len(buf)
            f.write(bytes(buf))

        interval_time = time.time() - start
        if interval_time >= 1:
            speed = len_log / interval_time
            print(speed / 1000, 'KB/S')
            len_log = 0


# print(dir(s))
# print(help(s.send))
