"""
"""
import itertools
import random
import copy

s1 = 'L'
s2 = 'U'
s3 = 'R'
s4 = 'D'
class CMuncher(object): 
	"""
	"""	
		
	def __init__(self):	
		self.counter = 0
	def routeLine(self, startNode, startTime):
		self.startNode = startNode
		self.startTime = startTime
		permutation = "LURD"
		result = str(self.startTime)+" "+str(self.startNode.x)+" "+str(self.startNode.y)+" "+permutation
		return result
	
	def route(self, graph, starter, permutation):		
		perm = itertools.cycle(permutation)
		n = []
		startTime = self.counter
		while starter.neighborsLeft() != 0:
			n.append(starter.id)
			starter.eaten = True
			starter = self._next(perm, starter)
			self.counter+=1	
		n.append(starter.id)
		starter.eaten = True
		#print "timeCounter: ", startTime, " nodes: ", n, " permutation: ", permutation
		return (startTime)
		
	def gene(self, graph, times):
		populations = []
		for i in range(times):
			schedule = CMuncher().unregular(graph)
			populations.append(None)
			populations[i] ={ "numberOfMunchers":len(schedule), "schedule":schedule}
		populations = sorted(populations, key = lambda pop: pop['numberOfMunchers'])
		return populations[0]['schedule']
		
	def unregular(self, cgraph):
		graph = copy.deepcopy(cgraph)
		munchers = []
		while graph.uneaten()[0] != 0:
			permutation = [s1, s3, s2, s4]
			random.shuffle(permutation)
			startAt = self._starter(graph)
			if len(startAt) != 0:
				random.shuffle(startAt)
				startNode = startAt[0]
			else:
				startNode = graph.uneaten()[1]
			startTime = self.route(graph, startNode, permutation)
			result = str(startTime)+" "+str(startNode.x)+" "+str(startNode.y)+" "+permutation[0]+permutation[1]+permutation[2]+permutation[3]
			munchers.append(result)
		return munchers

	def _next(self, perm, node):
		next = None
		while True:
			state = perm.next() 
			if state == 'L':
				if node.l != None and node.l.eaten == False:
					next = node.l
					break
			elif state == 'U':
				if node.u != None and node.u.eaten == False:
					next = node.u
					break
			elif state == 'R':
				if node.r != None and node.r.eaten == False:
					next = node.r
					break
			elif state == 'D':
				if node.d != None and node.d.eaten == False:
					next = node.d
					break
		return next
	def _starter(self, graph):
#		noid = []
		no = []
		for node in graph.nodes:
			if node.eaten == False:
				if node.neighborsLeft() == 1:
#					noid.append(node.id)
					no.append(node)
#		print noid					
		return no
