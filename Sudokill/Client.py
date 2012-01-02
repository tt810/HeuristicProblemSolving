import socket
import sys
from Board import *

"""
ruby player.rb 8080 T
"""
HOST = "localhost"
PORT = int(sys.argv[1])
NAME = sys.argv[2]

#Connect: 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send("SUDOKILL_PLAYER\n")
s.send(NAME+'\n')

def msg(move):
	x, y, num = move[0], move[1], move[2]
	msg = str(x)+' '+str(y)+' '+str(num)+'\n'
	print "msg: ", msg
	return msg
	
while True:
	"""
MOVE START
1 0 7
0 4 2
6 5 5
5 6 7
0 5 7
3 6 1
8 3 3
2 5 8
2 7 1
-1 -1 -1
MOVE END
['6 7 7', '7 2 4', '5 0 6', '5 7 9', '2 3 5', '-1 -1 -1']
	"""
	data = s.recv(1024)
	print data
	data = data.split('\n')[1:-2]
	print data
	boardInfo = []
	for strInfo in data:
		boardInfo += [[int(p) for p in strInfo.split(' ')]]
	print boardInfo
	board = Board(boardInfo)
	mymove = board.makeMove()
	print "my move: ", mymove
	s.send(msg(mymove))
s.close()
