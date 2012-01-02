# Echo client program
import socket
import time, sys

HOST = sys.argv[1]    # The remote host
PORT = int(sys.argv[2])        # The same port as used by the server
M = int(sys.argv[3])
N = int(sys.argv[4])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
	data = s.recv(1024)
	if data == "END":
		break
	print data
	mv = raw_input("Input move:\n")
	s.send(mv)

s.close()
