import socket
import time, sys
from random import choice

HOST = sys.argv[1]
PORT = int(sys.argv[2])
M = int(sys.argv[3])
N = int(sys.argv[4])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

h_move_forward = "Remove:[] Build: Remove:[] Build:"

def remove_wall(walls):
	return "Remove:[] "
	
while True:
	data = s.recv(1024)
	if data == "END":
		break
	print data
	lines = data.split("\n")
	print "Input move:\n"	
	hunter = lines[1].split(":")
	hcoords = hunter[1].split(" ")
	hx, hy = int(hcoords[0]), int(hcoords[1])
	hdx, hdy = int(hcoords[2]), int(hcoords[3])
	prey = lines[2].split(":")
	pcoords = prey[1].split(" ")
	px, py = int(pcoords[-2]), int(pcoords[-1])
	def above_prey(lists):
		lis = []
		for lst in lists:
			if lst[2] < py:
				lis.append(lst)
		return lis
	def under_prey(lists):
		lis = []
		for lst in lists:
			if lst[2] > py:
				lis.append(lst)
		return lis
	def left_prey(lists):
		lis = []
		for lst in lists:
			if lst[1] < px:
				lis.append(lst)
		return lis
	def right_prey(lists):
		lis = []
		for lst in lists:
			if lst[1] > px:
				lis.append(lst)
		return lis
	def remove_wall(walls):
		remove = []
		wall = walls.split(", ")
		if len(wall) % 4 == 0:
			index = x1 = y1 = x2 = y2 = 0
			howl = []
			vewl = []			
			for i in range(len(wall)):
				if i % 4 == 0:
					indx = wall[i].split(" ")[0].split("[")[-1]
					index=int(indx)
					x = wall[i].split(" ")[1].split("(")[-1]
					x1=int(x)
				elif i % 4 == 1:
					y1=int(wall[i])
				elif i % 4 == 2:
					x2=int(wall[i])
				elif i % 4 == 3:
					y = wall[i].split(")")[0]
					y2 = int(y)
					if x1 == x2:
						vewl.append([index, x1, y1, x2, y2])
					else:
						howl.append([index, x1, y1, x2, y2])
			if len(howl) > 1:
				above = above_prey(howl)
				under = under_prey(howl)
				if len(above) > 1:
					index = 0
					y = py
					for a in above:
						if a[2] < y:
							y = a[2]
							index = a[0]
					remove.append(index)
				if len(under) > 1:
					index = 0
					y = py
					for u in under:
						if u[2] > y:
							y = u[2]
							index = u[0]
					remove.append(index)
			if len(vewl) > 1:
				left = left_prey(vewl)
				right = right_prey(vewl)
				if len(left) > 1:
					index = 0
					x = px
					for l in left:
						if l[1] < x:
							x = l[1]
							index = l[0]
					remove.append(index)
				if len(right) > 1:
					index = 0
					x = px
					for r in right:
						if r[1] > x:
							x = r[1]
							index = r[0]
					remove.append(index)
			return "Remove:"+str(remove)+" "
		else:
			return "Remove:[] "
		
	
	if lines[0] == "You are Hunter":
		msg = h_move_forward
		remove = remove_wall(lines[3].split(": ")[1])
		print remove
		if hx==218 and hy==218 and hdx==1 and hdy==1:
			msg = remove + "Build:1 0 499 Remove:[] Build:"
		if hx > 218 and (hy-py)*hdy < 0:
			print hx, " ", hy, " ", py, " ", hdy
			msg = remove + "Build:0 219 499 Remove:[] Build:"
#		if hx > 218 and (hx-px)*hdx < 0:
#			print hx, " ", hy, " ", px, " ", hdx
#			msg = remove + "Build:1 1 499 Remove:[] Build:"
		
		s.send(msg)
	else:
		delta_x = [-1, 0, 1]
		delta_y = [-1, 0, 1]
		mv = str(choice(delta_x))+" "+str(choice(delta_y))
		
		if px != 219 and py != 500:
			mv = "-1 0"
		elif px == 219 and py!=500:
			mv = "0 1"
		else:
			mv = "-1 0"
		
		s.send(mv)
		
s.close()
