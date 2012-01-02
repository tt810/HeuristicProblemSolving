"""
"""
import itertools
import random
import copy

s1 = 'L'
s2 = 'U'
s3 = 'R'
s4 = 'D'
class Muncher(object): 
	"""
	"""	
		
	def __init__(self, startNode, startTime):	
		self.startNode = startNode
		self.startTime = startTime
	def routeLine(self):
		permutation = "LURD"
		result = str(self.startTime)+" "+str(self.startNode.x)+" "+str(self.startNode.y)+" "+permutation
		return result
	
	def route(self, graph, starter, permutation, startTime):		
		perm = itertools.cycle(permutation)
		n = []
		count = 0
		while starter.neighborsLeft() != 0:
			n.append(starter.id)
			starter.eaten = True
			starter = self._next(perm, starter)
			count+=1	
		n.append(starter.id)
		starter.eaten = True
		count += 1
		#print "timeCounter: ", startTime, " nodes: ", n, " permutation: ", permutation
		return (count)
	
	def unregular(self, cgraph):
		graph = copy.deepcopy(cgraph)
		munchers = []		
		lastCount = 0
		while graph.uneaten()[0] != 0:
			starts = self._starter(graph)
			if len(starts) > 1:
				startTime = [lastCount for start in starts[:2]]
				random.shuffle(starts)	
				count = []
				#print lastCount," lastCount"			
				for i, start in enumerate(starts[:2]):
					permutation = [s1, s3, s2, s4]
					random.shuffle(permutation)
					result = str(startTime[i])+" "+str(start.x)+" "+str(start.y)+" "+permutation[0]+permutation[1]+permutation[2]+permutation[3]
					munchers.append(result)
					count.append(self.route(graph, start, permutation, startTime[i]))	
			#	print count, " count"			
				lastCount = lastCount + sorted(count)[-1]
			elif len(starts) == 1:
				startTime = lastCount
				permutation = [s1, s3, s2, s4]
				random.shuffle(permutation)
				result = str(startTime)+" "+str(start.x)+" "+str(start.y)+" "+permutation[0]+permutation[1]+permutation[2]+permutation[3]
				munchers.append(result)
				lastCount = self.route(graph, starts[0], permutation, startTime) + lastCount
			#	print lastCount," last Count in side1"
			else:
				startTime = lastCount
				permutation = [s1, s3, s2, s4]
				random.shuffle(permutation)
				start = graph.uneaten()[1]
				result = str(startTime)+" "+str(start.x)+" "+str(start.y)+" "+permutation[0]+permutation[1]+permutation[2]+permutation[3]
				munchers.append(result)
				lastCount = self.route(graph, start, permutation, startTime) + lastCount
			#	print lastCount," last Count in side2"
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
	#	noid = []
		no = []
		for node in graph.nodes:
			if node.eaten == False:
				if node.neighborsLeft() == 1:
	#				noid.append(node.id)
					no.append(node)
	#	print noid					
		return no
