#!/usr/bin/env python3
import socket

if __name__ == '__main__':
	hostname = 'www.python.org'
	addr = socket.gethostbyname(hostname)
	print('The Ip address of {} is {}'.format(hostname, addr))