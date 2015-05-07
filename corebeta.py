import random
import math


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
			cumulator *= (n-k)/(k+1)
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

	def __init__(self, reactants, products, name, colonies):
		"""
		Description of object in class reaction. 

		Variables type:
		reactants - dictionary
		products - dictionary
		name - string
		colonies - list of colony objects

		Comments:
		Keys of the dictionaries rectants and products should be named accoring to colonies names.
		Important for the class gillespie implementation.

		Usage example:
		Reaction of type X + X -> Y can be written as
		>> X = colony('Xome',24)
		>> Y = colony('Yome',56)
		>> R = reaction({'Xome': 2},{'Yome': 1}, 'conversion', [X, Y])
		"""
		self.name = name
		self.reactants = reactants
		self.products = products
		self.colonies = colonies

class gillespie:
	"""
	Algorithm of a stochastic simulation.
	"""
	def __init__(self, reactions):
		"""
		Description of object in class gillespie.

		Variables type:
		reactions - list of reaction objects

		Usage example:
		>> R1 = reaction({'X': 2},{'Y': 1}, 'X conversion', [X, Y])
		>> R2 = reaction({'Z': 3},{'Y': 4}, 'Z conversion', [X, Y])
		>> G = gillespie([R1, R2])
		"""
		self.reactions = reactions

	def probability(self):
		"""
		Calculation of reactions propensities.
		"""
		a0 = 0
		a = []
		for reaction in self.reactions:
			for colony in reaction.colonies:
				name = colony.name
				try:
					num = reaction.reactants[name]
					prob = choose(num, colony.size)
					a.append(prob)
					a0 += prob
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
		"""
		data = {}

		step = 0
		while step < steps:
			a0, a = self.probability()
			reactnum = choosereaction(a0, a)
			timestep = calctimestep(a0)

			for colony in self.reactions[reactnum].colonies:
				if colony.name in self.reactions[reactnum].reactants:
					colony.size -= self.reactions[reactnum].reactants[colony.name]
				if colony.name in self.reactions[reactnum].products:
					colony.size += self.reactions[reactnum].products[colony.name]			

			step += 1

		return data









































