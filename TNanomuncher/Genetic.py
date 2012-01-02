from CMuncher import *
import random

class Genetic(object):
	
	def __init__(self, times):

		self.times = times
	"""
	def genePopulations(self, node, graph):
		self.populations = []
		for i in range(self.times):
			schedule = CMuncher(node, 0).unregular(graph)
			self.populations.append(None)
			self.populations[i] ={ "numberOfMunchers":len(schedule), "schedule":schedule}
		self.populations = sorted(self.populations, key = lambda pop: pop['numberOfMunchers'])
		return self.populations[0]['schedule']
	"""
	def genePopulations(self, graphs):
		munchers = []
		if len(graphs) == 1:
			munchers = CMuncher().gene(graphs[0], 500)
		else:
			self.populations = []
			for i in range(self.times):
				num = 0
				graphd = {}
				for j, graph in enumerate(graphs):
					schedule = CMuncher().gene(graph, self.times)
					num = num + len(schedule)
					graphd['graph'+str(j)] = (graph, schedule)
				self.populations.append(None)
				graphd['numberOfMunchers'] = num
				#print "i: ", i,graphd
				self.populations[i] = graphd
			self.populations = sorted(self.populations, key = lambda pop: pop['numberOfMunchers'])
			best = self.populations[0]
			for j in range(len(graphs)):
				munchers = munchers + best['graph'+str(j)][1]
		return munchers
			
		
	
