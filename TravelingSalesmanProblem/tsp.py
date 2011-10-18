import math
import copy
import itertools
import sys
from collections import deque

def makeGraph(fileName): 
	def reader():
		"""
		Read the text file and process it
		"""
		listCity = []
		with open(fileName, 'r') as f:
			listCity = [line.split(' ') for line in f.read().split('\n')]
		return filter(lambda x: x!=[''], listCity)

	def distance(a, b):
		""" 
		Compute distance between node A and node B
		"""
		return math.sqrt(sum([math.pow((int(x)-int(y)), 2) for x, y in zip(a,b)[1:]]))
	
	def computeDistance(): 
		"""
		Compute all distances from all cities
		"""
		cities = reader()
		yield ''
		for i in range(0, len(cities)):
			di = {}
			for j in range (i+1, len(cities)):
				di[j+1] = distance(cities[i], cities[j])
			yield di
			
	return computeDistance()

"""
-------------
"""

class TSP(object): 
	"""
	"""
	
	def __init__ (self, fileName): 
		#MST Var
		self.G = list(makeGraph(fileName))
		self.mst = self.minimumSpanningTree(self.G, len(self.G))
		self.undirectedMst, self.directedMst = self.mst[0], self.mst[1]		
		

	@staticmethod
	def minimumSpanningTree(G, numberOfNodes):
		"""
		Return the minimum spanning tree of an undirected graph G.
		G should be represented in such a way that G[u][v] gives the
		length of edge u,v, and G[u][v] should always equal to G[v][u].
		The tree is returned as a list of edges.
		"""
		subtrees = UnionFind()
		directedTree, undirectedTree = {}, {}
		edges = [(G[x][y], x, y)for x in range(1, numberOfNodes) for y in range (x+1, numberOfNodes)]
		edges.sort()
		for distances,u,v in edges:
			if subtrees[u] != subtrees[v]:
				if not undirectedTree.has_key(str(u)): undirectedTree[str(u)] = []
				if not directedTree.has_key(str(u)): directedTree[str(u)] = []
				if not undirectedTree.has_key(str(v)): undirectedTree[str(v)] = []
				undirectedTree[str(u)].append(v)
				undirectedTree[str(v)].append(u)
				directedTree[str(u)].append(v)
				subtrees.union(u,v)
		return undirectedTree,directedTree 
	
	def sortOdds(self):
		odds = [(len(self.undirectedMst[keys]), keys) for keys in self.undirectedMst.iterkeys() if len(self.undirectedMst[keys]) % 2 != 0]
		stack = sorted(odds)
		return stack

	def inMstTree(self, x, y):
		undirectedmst = self.undirectedMst
		return y in undirectedmst[str(x)]
    
	def addEdgetoMST(self, x, y):
		if y<x: x, y = y, x
		self.undirectedMst[str(x)].append(y) 
		self.undirectedMst[str(y)].append(x)
    	
	def mwm(self):
	"""
	minimum weigth matching, after minimum spanning tree, 
	make sure every node has even degrees.
	"""
		odds = self.sortOdds()
		sortodds = []
		while odds != []:
			sortodds.append(int(odds.pop()[1]))
		while sortodds != []:
			edges = []
			for i in range(1, len(sortodds)):
				length = 0.0
				if sortodds[0] < sortodds[i]: 
					length = self.G[sortodds[0]][sortodds[i]]
				else:
					length = self.G[sortodds[i]][sortodds[0]]
				edges += [(length, sortodds[0], sortodds[i])]
			edge = min(edges)
			self.addEdgetoMST(edge[1], edge[2])
			sortodds.remove(edge[1])
			sortodds.remove(edge[2])

	def getEulerPath(self): 
		"""
		Return the euler path of a mst and mwm tree. 
		"""
		#Euler Var
		self.nodesToGoTo = deque([])
		self.eulerGraph = copy.deepcopy(self.undirectedMst)
		self.euler = Euler()
		#Euler Funct
		self.__randomPath()
		self.eulerGraph = self.euler()
		#cast eulerGraph nodes to int: 
		self.eulerGraph = [int(nodes) for nodes in self.eulerGraph]
		
	def getK_opt(self):
		self.kopt = K_opt(self.undirectedMst, self.eulerGraph, self.G)
		
	def __randomPath(self, key = None): 
		"""
		Take a random path such that each edge can only be used once. 
		The function is stopped when no more edges can be taken
		"""
		if key == None: 
			it = iter(self.eulerGraph)
			key = it.next()
			while len(self.eulerGraph[key]) == 0: key = it.next() 
		subPath = []
		subPath.append(key)
		
		while len(self.eulerGraph[str(key)]) != 0: 
			#check if several edges: 
			if len(self.eulerGraph[str(key)])>1:
				#if several egdes, take the first one: 
				self.nodesToGoTo.append(key)
			subPath.append(self.eulerGraph[str(key)][0])
			oldKey, key = str(key), self.eulerGraph[str(key)][0]
			#Delete edges	
			del(self.eulerGraph[oldKey][0])
			self.eulerGraph[str(key)].remove(int(oldKey))
	
		self.euler.addSubPath(subPath)		
		if len(self.nodesToGoTo) > 0: 
			#recursive call
			key = str(key)
			while len(self.eulerGraph[key]) == 0:
				if len(self.nodesToGoTo) == 0: break
				key = str(self.nodesToGoTo.popleft()) 
			
		if len(self.eulerGraph[key]) > 0: self.__randomPath(key)	
	
	def __call__(self): 
		#Mwm
		self.mwm()
		self.getEulerPath()
		self.getK_opt()
		return self.kopt.opt2()
		
"""
-------------
"""		

class Euler(object): 
	"""
	A Sub Path is a data structure, 
	A Sub Path is an euler path complete or not. 
	Support several operations like merging. 
	"""
	
	def __init__ (self): 
		self.eulerSubPaths = []
	
	
	def addSubPath (self, subPath): 
		"""
		@param subPath: list of nodes forming an euler sub path 
		Once added, the subPath are merged if possible
		"""		
		self.eulerSubPaths.append(subPath)
		
		#merge operation
		if len(self.eulerSubPaths) >1: 
			#if path can be merged, merged
			indexes = (self.eulerSubPaths[0].index(int(self.eulerSubPaths[1][0])), 0)
			self.eulerSubPaths[0] = self.eulerSubPaths[0][:(indexes[0])]+ self.eulerSubPaths[1][indexes[1]:] + self.eulerSubPaths[0][(indexes[0]+1):]
			del(self.eulerSubPaths[1])
			
	def isEuler(self, graph): 
		"""
		Return true if all nodes from the given have an even degree
		Return false otherwise
		"""
		oddNodes = [nodes for nodes in graph if len(nodes)%2 !=0]
		if oddNodes>0: return False
		return True

	def __call__(self): 
		return self.eulerSubPaths[0]

"""
-------------
"""

class K_opt(object): 
	
	def __init__ (self, undirectedGraph, eulerTour, G): 
		"""
		@param: euler tour is a list of nodes 
		@param: undirectedGraph is a the last version generated by the TSP instance for the graph
		"""
		self.eulerTour = eulerTour
		self.undirectedGraph = undirectedGraph
		self.G = G
		self.distance()
		
	def getInit(self):
		#nodepairs = [(key, len(self.undirectedGraph[key])) for key in self.undirectedGraph.iterkeys() if len(self.undirectedGraph[key]) != 2]
		nodepairs = [(node, self.eulerTour.count(node)) for node in self.eulerTour if self.eulerTour.count(node) >= 2]
		nodepairs = set(nodepairs)
		for nodepair in nodepairs:
			node = nodepair[0]
			number = nodepair[1]
			while number!= 1:
				index = self.eulerTour.index(int(node))
				self.eulerTour.pop(index)				
				number -= 1
		last = self.eulerTour[-1]
		self.eulerTour.insert(0, last)
	def distance(self):
		"""
		Return the dist of the tour
		"""
		dis = 0
		for i in range(len(self.eulerTour)-1): 
			dis += self.dist(self.eulerTour[i], self.eulerTour[i+1])
		return dis
		
	def dist(self, x, y):
		if x>y: x, y = y, x
		return self.G[x][y]
		
	def opt2(self): 
		self.getInit()
		number = 4
		while number != 0:
			for i in range(0, len(self.eulerTour)-3):
				for j in range(i+2, len(self.eulerTour)-1):
					a1 = self.eulerTour[i]
					a2 = self.eulerTour[i+1]
					b1 = self.eulerTour[j]
					b2 = self.eulerTour[j+1]
					if self.dist(a1, a2)+self.dist(b1, b2) > self.dist(a1, b1)+self.dist(a2, b2):
						self.eulerTour[i+1], self.eulerTour[j] = b1, a2
						gap = j-(i+1)
						if gap > 2:
							li = [self.eulerTour[k] for k in range(i+2, j)]
							h = j-i-3
							for k in range(i+2, j):							
								self.eulerTour[k] = li[h]
								h -= 1
			number -= 1	
		print self.distance()
		print self.eulerTour
		
		
	def __call__(self):
		return opt2()
	

	
"""
-------------
"""		

class UnionFind(object):
    """Union-find data structure.

    Each unionFind instance X maintains a family of disjoint sets of
    hashable objects, supporting the following two methods:

    - X[item] returns a name for the set containing the given item.
      Each set is named by an arbitrarily-chosen one of its members; as
      long as the set remains unchanged it will keep the same name. If
      the item is not yet part of a set in X, a new singleton set is
      created for it.

    - X.union(item1, item2, ...) merges the sets containing each item
      into a single larger set.  If any item is not yet part of a set
      in X, it is added to X as one of the members of the merged set.
    """

    def __init__(self):
        """Create a new empty union-find structure."""
        self.weights = {}
        self.parents = {}

    def __getitem__(self, object):
        """Find and return the name of the set containing the object."""

        # check for previously unknown object
        if object not in self.parents:
            self.parents[object] = object
            self.weights[object] = 1
            return object

        # find path of objects leading to the root
        path = [object]
        root = self.parents[object]
        while root != path[-1]:
            path.append(root)
            root = self.parents[root]

        # compress the path and return
        for ancestor in path:
            self.parents[ancestor] = root
        return root
        
    def __iter__(self):
        """Iterate through all items ever found or unioned by this structure."""
        return iter(self.parents)

    def union(self, *objects):
        """Find the sets containing the objects and merge them all."""
        roots = [self[x] for x in objects]
        heaviest = max([(self.weights[r],r) for r in roots])[1]
        for r in roots:
            if r != heaviest:
                self.weights[heaviest] += self.weights[r]
                self.parents[r] = heaviest

if __name__ == "__main__": 
	fileName = sys.argv[1]
	results = TSP(fileName)()
	
	
