from socket import socket, gethostbyname, AF_INET, SOCK_STREAM
import time
import datetime
import sqlite3
import os
import http.client
import sys
import porttest


target = "localhost"
port = 80



filedb = 'porttest.sqlite'


if (len(sys.argv) < 2) or (len(sys.argv) > 3): 
	print ('Usage: porttest.py stat ')
	print ('  or   porttest.py report yyyymmdd')
	exit(0)


conn = porttest.connect(filedb)

param1 = sys.argv[1]


if param1 == 'stat' :
	while True:
		porttest.stat(conn, target, port)		
		time.sleep(60)

if param1 == 'report':
	param2 = sys.argv[2]
	porttest.report1(conn,param2)
