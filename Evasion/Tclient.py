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
	def get_walls(walls):
		howl = [[-1, 0, -1, 500, -1], [-2, 0, 500, 500, 500]]
		vewl = [[-1, 500, -1, 500, 500]]
		wall = walls.split(", ")
		if len(wall) % 4 == 0:
			index = x1 = y1 = x2 = y2 = 0
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
		return (howl, vewl)
	def remove_wall(howl, vewl, walls):
		remove = []	
		wall = walls.split(", ")
		if M >= 4:
			if len(howl) > 3:
				above = above_prey(howl)
				under = under_prey(howl)
				if len(above) > 2:
					index = 0
					y = py
					for a in above:
						if a[0] != -1 and a[0] != -2 and a[2] < y:
							y = a[2]
							index = a[0]
					remove.append(index)
				if len(under) > 2:
					index = 0
					y = py
					for u in under:
						if u[0] != -1 and u[0] != -2 and u[2] > y:
							y = u[2]
							index = u[0]
					remove.append(index)				
			if len(vewl) > 2:
				left = left_prey(vewl)
				right = right_prey(vewl)
				if len(left) > 1:
					index = 0
					x = px
					for l in left:
						if l[0] != -1 and l[1] < x:
							x = l[1]
							index = l[0]
					remove.append(index)
				if len(right) > 2:
					index = 0
					x = px
					for r in right:
						if r[0] != -1 and r[1] > x:
							x = r[1]
							index = r[0]
					remove.append(index)
			return "Remove:"+str(remove)+" "
		elif M == 2:
			if len(howl) == 3:
				above = above_prey(howl)
				under = under_prey(howl)
				if len(above) > 1:
					index = 0
					y = py
					for a in above:
						if a[0] != -1 and a[0] != -2:
							y = a[2]
							index = a[0]
					remove.append(index)
				elif len(under) > 1:
					index = 0
					y = py
					for u in under:
						if u[0] != -1 and u[0] != -2:
							y = u[2]
							index = u[0]
					remove.append(index)
			return "Remove:"+str(remove)+" "
	def build_vertical(howl):
		above = above_prey(howl)
		under = under_prey(howl)
		print above,"************a"
		print under, "***************u"
		min_y = 0
		max_y = 500
		if len(above) >0:
			for a in above:
				if a[2] > min_y:
					min_y = a[2]
		min_y = min_y + 1
		if len(under)>0:
			for u in under:
				if u[2] < max_y:
					max_y = u[2]
		max_y = max_y - 1
		print min_y," miny", max_y," maxy"
		return (min_y, max_y)
	def build_horizontal(vewl):
		left = left_prey(vewl)
		right = right_prey(vewl)
		min_x = 0
		max_x = 500
		print "left: ", left
		print "right: ", right
		if len(left) >0:
			for l in left:
				print l,"****l"
				if l[1] > min_x:
					min_x = l[1]
		print min_x," minx"
		min_x = min_x + 1
		if len(right) >0:
			for r in right:
				print r, "****r"
				if r[1] < max_x:
					max_x = r[1]
		print max_x, " maxx"
		max_x = max_x - 1 
		return (min_x, max_x)
#		return "Build:0 "+str(min_x)+" "+str(max_x)+" "
	
	if lines[0] == "You are Hunter":
		msg = h_move_forward
		(howl, vewl) = get_walls(lines[3].split(": ")[1])
		print howl,"*********",vewl
		remove = remove_wall(howl, vewl, lines[3].split(": ")[1])
		print remove
		(min_x, max_x) = build_horizontal(vewl)
		(min_y, max_y) = build_vertical(howl)
		if M >= 4:
			if hx==218 and hy==218 and hdx==1 and hdy==1:
				msg = remove + "Build:1 0 499 Remove:[] Build:"		
			if hx > 218 and (hy-py)*hdy < 0 and (max_x - min_x)>=(max_y - min_y):
				print "&&&&&&&&"
				build = "Build:0 "+str(min_x)+" "+str(max_x)+" "
				print build
				msg = remove + build + "Remove:[] Build:"
			elif hx > 218 and (hx-px)*hdx < 0 and (max_x - min_x) < (max_y - min_y):
				print "%%%%%%%%%%%%%%%"
				build = "Build:1 "+str(min_y)+" "+str(max_y)+" "
				print build
				msg = remove + build + "Remove:[] Build:"
		elif M == 2:
			if hx==218 and hy==218 and hdx==1 and hdy==1:
				msg = remove + "Build:1 0 499 Remove:[] Build:"	
			if hx > 218 and (hy-py)*hdy < 0:
				build = "Build:0 "+str(min_x)+" "+str(max_x)+" "
				msg = remove + build + "Remove:[] Build:" 
		s.send(msg)
	else:
		delta_x = [-1, 0, 1]
		delta_y = [-1, 0, 1]
		mv = str(choice(delta_x))+" "+str(choice(delta_y))
		"""
		if px != 219 and py != 0:
			mv = "0 -1"
		elif px == 219 and py!=0:
			mv = "0 1"
		else:
			mv = "-1 0"
		"""
		s.send(mv)
		
s.close()
