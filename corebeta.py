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
		Keys of the dictionaries rectants and products should be named accoring to colonies names.
		Important for the class gillespie implementation.

		Usage example:
		Reaction of type X + X -> Y can be written as
		>> X = colony('Xome',24)
		>> Y = colony('Yome',56)
		>> R = reaction({'Xome': 2},{'Yome': 1}, 'conversion', [X, Y], 0.5)
		"""
		self.name = name
		self.reactants = reactants
		self.products = products
		self.colonies = colonies
		self.rate = rate

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
			for colony in reaction.colonies:
				name = colony.name
				try:
					num = reaction.reactants[name]
					prob = choose(colony.size, num)*reaction.rate
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
		Perform stochstic simulation
		"""
		data = {}
		for colony in self.colonies:
			data[colony.name] = []
			data[colony.name].append(colony.size)

		step = 0
		while step < steps:
			a0, a = self.probability()
			reactnum = self.choosereaction(a0, a)
			timestep = self.calctimestep(a0)

			for colony in self.reactions[reactnum].colonies:
				if colony.name in self.reactions[reactnum].reactants:
					colony.size -= self.reactions[reactnum].reactants[colony.name]
				if colony.name in self.reactions[reactnum].products:
					colony.size += self.reactions[reactnum].products[colony.name]			

			for colony in self.colonies:
				data[colony.name].append(colony.size)

			step += 1

		return data




import matplotlib.pyplot as plt
import numpy as np

H = colony('H', 0)
H2 = colony('H2', 1000)
R1 = reaction({'H': 1},{'H2': 1}, 'Binding', [H, H2], 0.5)
R2 = reaction({'H2': 1},{'H': 1}, 'Degradation', [H, H2], 0.5)
G = gillespie([R1, R2], [H, H2])
data = G.run(10000)
plt.plot(np.array(data['H']))
plt.show()
    

progenitors = []
peripheral = []
reactions = []
for clone in range(10):
    progenitors.append(colony('progenitor'), 0)
    peripheral.append(colony('peripheral', 0))
    reactions.append(reaction({}, {}, 'StemDiff', [], 0.1))
    reactions.append(reaction({}, {}, 'Renew', [], 0.1))
    reactions.append(reaction({}, {}, 'BloodCreat', [], 0.1))
    reactions.append(reaction({}, {}, 'ProgDeath', [], 0.1))
    reactions.append(reaction({}, {}, 'PeriphDeath', [], 0.1))


    C = Colony("Base", 0)
    R1 = Reaction("Renew", [C], [C,C], p)
    R2 = Reaction("Death", [C], [], muP)
    R3 = Reaction("BloodCreat", [C], [], omega)
    R4 = Reaction("StemDiff", [], [C], alpha)
    reactions = [R1, R2, R3, R4]
    
    # Create colonies for the simulation
    colonies = []
    for ind in range(numCol):
        numCells = 0
        colonies.append(Colony("P{0}".format(ind), numCells))
    
    gillespieSim = Gillespie(reactions, colonies)
    gillespieSim.run(timeLength)





































