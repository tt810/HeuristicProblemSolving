"""
"""

class Graph(object): 
	"""
	"""
	def __init__(self): 
		self.nodes = []

	def addNode(self, node): 
		"""
		"""
		self.nodes.append(node)
	
	def uneaten(self):
		count = 0
		startNode = None
		for node in self.nodes:
			if node.eaten == False: 
				count += 1
				startNode = node
		return (count, startNode)
	
	def isLine(self): 
		"""
		"""
		def isSimpleLine():
			start = self.nodes[0].id
			for node in self.nodes: 
				if node.numberOfNeighbors >2:
					return -1
				if node.numberOfNeighbors == 1: 
					start = node.id
			return start

		result = isSimpleLine()
		if result != -1: 
			return result
		else: 
			#Extra check:
			counter1=0
			counter3=0
			start = self.nodes[0].id 
			for node in self.nodes: 
				if node.numberOfNeighbors == 3:
					counter3 +=1
					if counter3 >1: return -1
				if node.numberOfNeighbors == 4: 
					return -1
				if node.numberOfNeighbors == 1: 
					start = node.id
					counter1 +=1
					if counter1>1: return -1
			if counter3 != 1 or counter1 != 1: 
				return -1
			return start
