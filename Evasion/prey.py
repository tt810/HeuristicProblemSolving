"""
delta_x = [-1, 0, 1]
		delta_y = [-1, 0, 1]
		mv = str(choice(delta_x))+" "+str(choice(delta_y))
		s.send(mv)
"""

class prey(object):
	def __init__(self):
		self.deltax = [-1, 0, 1]
		self.deltay = [-1, 0, 1]
		self.coords = [self.x, self.y]
		walls = []
	
	def play(self, hunter):
		mv = str(choice(delta_x))+" "+str(choice(delta_y))
		return mv
