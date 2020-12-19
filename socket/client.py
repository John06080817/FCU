# -*- coding: utf-8 -*-
import socket

HOST = "140.134.30.161"
PORT = 13000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while True:
	cmd = input("Please input msg:")
	s.send(cmd.encode('utf-8'))
	data = s.recv(1024)
	print(data.decode('utf-8'))
	
#123