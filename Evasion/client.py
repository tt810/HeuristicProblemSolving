import socket
import time, sys
from random import choice

HOST = sys.argv[1]
PORT = int(sys.argv[2])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
	data = s.recv(1024)
	if data == "END":
		break
	print data
	lines = data.split("\n")
	print "Input move:\n"
	if(lines[0] == "You are Hunter"):
		s.send("Remove:[] Build: Remove:[] Build:")
	else:
		delta_x = [-1, 0, 1]
		delta_y = [-1, 0, 1]
		mv = str(choice(delta_x))+" "+str(choice(delta_y))
		s.send(mv)
		
s.close()
