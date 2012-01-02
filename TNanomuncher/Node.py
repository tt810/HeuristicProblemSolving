"""
"""

class Node(object): 
	"""
	"""
	
	def __init__ (self, id, x, y): 
		"""
		"""
		self.x = x
		self.y = y
		self.id = id
		self.u = None
		self.d = None
		self.r = None
		self.l = None
		self.numberOfNeighbors = 0
		self.eaten = False
		
	def makeEdge(self, node):
		"""
		@param node is node object
		"""
		
		if node.x == self.x: 
			if node.y < self.y: 
				self.d = node
				self.numberOfNeighbors+=1
				node.u = self
				node.numberOfNeighbors+=1
			if node.y > self.y: 
				self.u = node
				self.numberOfNeighbors+=1
				node.d = self
				node.numberOfNeighbors+=1
				
		elif node.y == self.y: 
			if node.x < self.x: 
				self.l = node
				self.numberOfNeighbors+=1
				node.r = self
				node.numberOfNeighbors+=1
			if node.x > self.x: 
				self.r = node
				self.numberOfNeighbors+=1
				node.l = self
				node.numberOfNeighbors+=1
		
	def neighborsLeft(self):
		"""
		if the muncher can not go anywhere from this node, then this node is a black hole
		In another words, the node doesn't have any uneaten neighbor
		"""
		count = 0
		if self.l != None and self.l.eaten == False:
			count += 1
		if self.u != None and self.u.eaten == False:
			count += 1
		if self.r != None and self.r.eaten == False:
			count += 1
		if self.d != None and self.d.eaten == False:
			count += 1
		return count
