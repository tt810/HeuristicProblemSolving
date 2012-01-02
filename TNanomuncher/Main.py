from Node import * 
from collections import deque
from Graph import * 
from Muncher import * 
from Genetic import *
import sys

nodes = []
graphs = []
munchers = []



def parse(fileName):
	"""
	@param filename: ...
	parse input text
	"""
	isNode = False
	isEdge = False
	f = open(fileName).read().split('\n')
	
	for line in f: 
		#Node Parsing: 
		if isNode ==True and line == "":
			isNode = False 
		elif isNode ==True: 
			data = line.split(',')
			nodes.append(Node(int(data[0]), int(data[1]), int(data[2])))		
	
		if line == "nodeid,xloc,yloc": isNode= True
		if line == "nodeid1,nodeid2": isEdge = True
	
		#Edge Parsing:
		elif isEdge == True and line!='': 
			data = line.split(',')
			nodes[int(data[0])].makeEdge(nodes[int(data[1])])

def traversal():
	"""
	Traversing the graph using depth first search: 
		Create a new graph object for each graph found
	"""

	#step 2: 
	def discover(i, k): 
		"""
		will discover node i and all possible neghbor in a recusrive way
		"""
		graphs[k].addNode(nodes[i])
		#Check alll neighbors		
		if nodes[i].l != None:
			if isRead[nodes[i].l.id] == False: 
				isRead[nodes[i].l.id] = True	 
				queue.append(nodes[i].l)
		
		if nodes[i].u != None:
			if isRead[nodes[i].u.id] == False:
				isRead[nodes[i].u.id] = True 	 
				queue.append(nodes[i].u)
	
		if nodes[i].r != None:
			if isRead[nodes[i].r.id] == False: 
				isRead[nodes[i].r.id] = True	 
				queue.append(nodes[i].r)
	
		if nodes[i].d != None:
			if isRead[nodes[i].d.id] == False: 
				isRead[nodes[i].d.id] = True	 
				queue.append(nodes[i].d)
		
		if len(queue) != 0: 
			n = queue.popleft()
			discover(n.id, k)
	
	#init
	isRead = [False for node in nodes]
	queue = deque()
	k = 0

	#step 1: 
	for i, read in enumerate(isRead): 
		if isRead[i] == False: 
			graphs.append(Graph())
			isRead[i] = True
			discover(i, k)
			k+=1

def dropMuncher(): 
	for graph in graphs: 
		nodeID = graph.isLine() 
		if nodeID != -1: 
			#drop monster for line or cycle or single node
			#munchers.append(Muncher(nodes[nodeID], 0, isLine=True))
			muncher = Muncher(nodes[nodeID], 0)
			munchers.append(muncher.routeLine())	
		else:
			#drop monsters for unregular shapes
			#submunchers = CMuncher(nodes[0],0).genePopulations(nodes[0], graph, 20)
			submunchers = Muncher(nodes[0],0).unregular(graph)
			#munchers = munchers + submunchers
			for munch in submunchers:
				munchers.append(munch)
			
	print len(munchers)
	for muncher in munchers:
		print muncher
	return munchers	

if __name__ == "__main__":
	args = sys.argv[1]
	parse(args)
	traversal()
	#print len(graphs), " length of graphs"
	dropMuncher()
			

			
			
			
