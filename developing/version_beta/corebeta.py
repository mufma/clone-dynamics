import random
import math
import json


def choose(n, k):
	"""
	Calculation of n choose k from combinatorics. Number of ways to choose k 
	objects from n objects.
	Variables type:
	n - integer
	k - integer
	Usage example:
	>> choose(5, 2)
	>> 10
	"""
	if n >= k:
		cumulator = 1
		for ind in range(k):
			cumulator *= (n-ind)/(ind+1)
		return cumulator
	else:
		return 0 


class colony:

	def __init__(self, name, size):
		"""
		Description of object in class colony
		Variables type:
		name - string
		size - integer
		Usage example:
		>> X = colony('Xome', 100)
		"""
		self.name = name
		self.size = size

class reaction:

	def __init__(self, reactants, products, name, colonies, rate):
		"""
		Description of object in class reaction. 
		Variables type:
		reactants - dictionary
		products - dictionary
		name - string
		colonies - list of colony objects
		rate - float

		Comments:
		- Keys of the dictionaries rectants and products should be named accoring to colonies names.
		Important for the class gillespie implementation.
		- params provides total cell count for the renew of progenitors. 
		
		Usage example:
		Reaction of type X + X -> Y can be written as
		>> X = colony('Xome',24)
		>> Y = colony('Yome',56)
		>> R = reaction({'Xome': 2, 'data':[X]},{'Yome': 1, 'data':[Y]}, 'conversion', [X, Y], 0.5)
		"""
		self.name = name
		self.reactants = reactants
		self.products = products
		self.colonies = colonies
		self.rate = rate
	
	def reactrate(self):
		if self.name == "Renew":
			total = 0
			capacity = 1000.0
			for colony in self.colonies:
				total += colony.size
			if (1.0-total/capacity)>=0:
				return self.rate*(1.0-(total/capacity))
			else:
				return 0
		else:
			return self.rate
			
		    


class gillespie:
	"""
	Algorithm of a stochastic simulation.
	"""
	def __init__(self, reactions, colonies):
		"""
		Description of object in class gillespie.
		Variables type:
		reactions - list of reaction objects
		Usage example:
		>> R1 = reaction({'X': 2},{'Y': 1}, 'X conversion', [X, Y], 0.5)
		>> R2 = reaction({'Z': 3},{'Y': 4}, 'Z conversion', [X, Y], 0.3)
		>> G = gillespie([R1, R2], [X, Y, Z])
		"""
		self.reactions = reactions
		self.colonies = colonies

	def probability(self):
		"""
		Calculation of reactions propensities.
		"""
		a0 = 0
		a = []
		for reaction in self.reactions:
			for colony in reaction.reactants['data']:
				name = colony.name
				try:
					num = reaction.reactants[name]
					prob = choose(colony.size, num)*reaction.reactrate()
					a.append(prob)
					a0 += prob
				except:
					pass
		return a0, a

	def choosereaction(self, a0, a):
		"""
		"""
		# Random number to choose reaction
		r = random.random()
		ind = 0
		tot = a[0]
		while tot < r*a0:
			ind += 1
			tot += a[ind]
		return ind

	def calctimestep(self, a0):
		"""
		Calculate timestep sampled from exponential distribution.
		"""
		r = random.random()

		return (1./a0)*math.log(1./r)

	def run(self, steps):
		"""
		Perform stochastic simulation
		"""
		data = {}
		for colony in self.colonies:
			data[colony.name] = []
			data[colony.name].append(colony.size)

		step = 1
		while step < steps:
			a0, a = self.probability()
			reactnum = self.choosereaction(a0, a)
			timestep = self.calctimestep(a0)
			
			for colony in self.reactions[reactnum].reactants['data']:
				name = colony.name
				colony.size -= self.reactions[reactnum].reactants[colony.name]
				
			for colony in self.reactions[reactnum].products['data']:
				name = colony.name
				colony.size += self.reactions[reactnum].products[colony.name]

			for colony in self.colonies:
				data[colony.name].append(colony.size)

			step += 1

		return data

def main():
	stem = []
	progenitors = []
	mature = []
	clones = 100
	
	for rep in range(clones):
	    stemname = 'stem{0}'.format(rep)
	    progname = 'progenitor{0}'.format(rep)
	    matname = 'mature{0}'.format(rep)
	    S = colony(stemname, 1)
	    P = colony(progname, 0)
	    M = colony(matname, 0)
	    stem.append(S)
	    progenitors.append(P)
	    mature.append(M)
	
	reactions = []
	for rep in range(clones):
		stemname = 'stem{0}'.format(rep)
		progname = 'progenitor{0}'.format(rep)
		matname = 'mature{0}'.format(rep)
		S = stem[rep]
		P = progenitors[rep]
		M = mature[rep]
		reactions.append(reaction({stemname:1, 'data':[S]}, {stemname:1, progname:1, 'data':[S, P]}, 'StemDiff', progenitors, 0.01))
		reactions.append(reaction({progname:1, 'data':[P]}, {progname:2, 'data':[P]}, 'Renew', progenitors, 1.0))
		reactions.append(reaction({progname:1, 'data':[P]}, {matname:1, 'data':[M]}, 'BloodCreat', progenitors, 0.2))
		reactions.append(reaction({progname:1, 'data':[P]}, {'data':[]}, 'ProgenitorDeath', progenitors, 0.2))
		reactions.append(reaction({matname:1, 'data':[M]}, {'data':[]}, 'MatureDeath', progenitors, 0.2))

	
	G = gillespie(reactions, mature)
	data = G.run(20000)
	jsondata = json.dumps(data)
	with open("resultsnew.txt", "w") as text_file:
	    text_file.write(jsondata)

import time
if __name__ == '__main__':
	start = time.time()
	main()
	end = time.time()
	print end-start