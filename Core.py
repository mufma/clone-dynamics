# -*- coding: utf-8 -*-
"""
Implementation of the Gillespie algorithm with classes. Architecture of the code is due to Paras Chopra (www.paraschopra.com).
"""
import random
import math

def choose(n, r):
    numerator = 1.0
    denominator = 1.0
    
    for i in range(1, r+1):
        numerator = numerator * (n-i+1)
        denominator = denominator * i

    return numerator/denominator

class Colony:
    
    def __init__(self, nameCol, sizeCol):
        self.name = nameCol
        self.size = sizeCol
    
class Reaction:
    
    def __init__(self, name, reactants, products, rate):
        self.name = name
        self.reactants = reactants
        self.products = products
        self.rate = rate

class Gillespie:
    
    def __init__(self, reactions, colonies):
        self.reactions = reactions
        self.colonies = colonies
        self.a0 = 0
        self.a = []
        self.t = 0
        self.timeArray = [0]
        
        self.data = {}
        for colony in self.colonies:
            self.data[colony.name] = [colony.size]
        
        # Record total cell number, so that later we can just update this
        # number, rather than going through all colonies on each step
        self.cellTotal = 0        
        
        for ind in range(len(self.colonies)):
            self.cellTotal += self.colonies[ind].size        
        
    def getParams(self):
        """
        Calculate propensities to choose timestep and reaction
        """
        self.a0 = 0
        self.a = []
        r1, r2 = random.random(), random.random()        
        
        for colony in self.colonies:
            for reaction in self.reactions:
                if reaction.name == 'Renew':
                    if (1.0 - self.cellTotal/1000.) < 0:
                        rate = 0.0
                    else:
                        rate = reaction.rate*(1.0 - self.cellTotal/1000.)
                else:
                    rate = reaction.rate
                # Since only one reactant 
                #numReactants = len(reaction.reactants)
                propensity = colony.size*rate
                if reaction.name == 'StemDiff':
                    propensity = rate

                self.a.append(propensity)
                self.a0 += propensity  
        
        # Choose timestep and reaction
        try:
            timestep = math.log(1./r1)/self.a0
        except:
            timestep = None
            print "All colonies are extinct."
        sum_of_as = 0.0
        ind = -1
        while sum_of_as < r2*self.a0:
            ind = ind + 1
            sum_of_as = sum_of_as + self.a[ind]
        numReact = len(self.reactions)
        
        # CHECK CORRECTNESS OF CHOICE colInd and reactInd
        colInd = ind/numReact
        reactInd = ind%numReact

        return colInd, reactInd, timestep
    
    def run(self, time):
        
        while self.t<time:
            colInd, reactInd, timestep = self.getParams()
            if timestep == None:
                print "break command is executed"
                break

            # Update colony
            reaction = self.reactions[reactInd]
            productNum = len(reaction.products)
            reactNum = len(reaction.reactants)
            self.colonies[colInd].size += productNum - reactNum
            self.cellTotal += productNum - reactNum
            
            for colony in self.colonies:
                self.data[colony.name].append(colony.size)            
            
            self.t += timestep
            self.timeArray.append(self.t)
            
        return self.timeArray, self.data


def Simulation(alpha, omega, muP, p, timeLength, numCol):
    # Colony "Base" is used to define reactions only
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
    
    return gillespieSim.timeArray, gillespieSim.data


def PropensityTestCase():
    """
    For the case below we expect to get 
    a0 = 100
    a = [22.5, 60.0, 7.5, 10.0]
    """
    C1 = Colony("Base", 10)
    C2 = Colony("Second", 6)
    R1 = Reaction("Renew", [C1,C1], [C1,C1], 0.5)
    R2 = Reaction("Update", [C1,C1,C1], [C1,C1], 0.5)
    reactions = [R1, R2]
    colonies = [C1, C2]
    gillespieSim = Gillespie(reactions, colonies)
    gillespieSim.getParams()
    print "Expected a0 = ", 100
    print "a0 = ", gillespieSim.a0
    print "Expected a = ", [22.5, 60.0, 7.5, 10.0]
    print "a = ", gillespieSim.a
    
def UpdateIncreaseTestCase():
    """
    For the case below we expect to update in one of the colonies.
    The number of cells should increase by 2
    """
    C1 = Colony("Base", 10)
    C2 = Colony("Second", 6)
    R1 = Reaction("Renew", [C1], [C1,C1,C1], 0.5)
    reactions = [R1]
    colonies = [C1, C2]
    gillespieSim = Gillespie(reactions, colonies)
    print "Before: ", C1.size, C2.size
    simLength = 1e-9
    gillespieSim.run(simLength)
    print "After: ", C1.size, C2.size
    print "Expect increase by 2"

def UpdateDecreaseTestCase():
    """
    For the case below we expect to update in one of the colonies.
    The number of cells should decrease by 3
    """
    C1 = Colony("Base", 10)
    C2 = Colony("Second", 6)
    R1 = Reaction("Renew", [C1,C1,C1,C1], [C1], 0.5)
    reactions = [R1]
    colonies = [C1, C2]
    gillespieSim = Gillespie(reactions, colonies)
    print "Before: ", C1.size, C2.size
    simLength = 1e-9
    gillespieSim.run(simLength)
    print "After: ", C1.size, C2.size
    print "Expect decrease by 3"

def UpdateEmptyDecreaseTestCase():
    """
    For the case below we expect to update in one of the colonies.
    The number of cells should decrease by 3
    """
    C1 = Colony("Base", 10)
    C2 = Colony("Second", 6)
    R1 = Reaction("Renew", [C1,C1,C1], [], 0.5)
    reactions = [R1]
    colonies = [C1, C2]
    gillespieSim = Gillespie(reactions, colonies)
    print "Before: ", C1.size, C2.size
    simLength = 1e-9
    gillespieSim.run(simLength)
    print "After: ", C1.size, C2.size
    print "Expect decrease by 3"

def UpdateEmptyIncreaseTestCase():
    """
    For the case below we expect to update in one of the colonies.
    The number of cells should increase by 2
    """
    C1 = Colony("Base", 10)
    C2 = Colony("Second", 6)
    R1 = Reaction("Renew", [], [C1,C1], 0.5)
    reactions = [R1]
    colonies = [C1, C2]
    gillespieSim = Gillespie(reactions, colonies)
    print "Before: ", C1.size, C2.size
    simLength = 1e-9
    gillespieSim.run(simLength)
    print "After: ", C1.size, C2.size
    print "Expect increase by 2"

def DataStoreTestCase():
    """
    For the case below we expect to update in one of the colonies.
    Then we store data in dictionary and expect to be like:
    {"Base": [10,12], "Second": [6,6]}
    or
    {"Base": [10,10], "Second": [6,8]}
    """
    C1 = Colony("Base", 10)
    C2 = Colony("Second", 6)
    R1 = Reaction("Renew", [], [C1,C1], 0.5)
    reactions = [R1]
    colonies = [C1, C2]
    gillespieSim = Gillespie(reactions, colonies)
    simLength = 1e-9
    gillespieSim.run(simLength)
    print "Expected:"
    print {"Base": [10,12], "Second": [6,6]}, "or"
    print {"Base": [10,10], "Second": [6,8]}
    print "Actual:"
    print gillespieSim.data
    
def SaturationTestCase(alpha, omega, muP, p, timeLength, numCol):
    # Colony "Base" is used to define reactions only
    C = Colony("Base", 0)
    R1 = Reaction("Renew", [C], [C,C], p)
    R2 = Reaction("Death", [C], [], muP)
    R3 = Reaction("BloodCreat", [C], [], omega)
    R4 = Reaction("StemDiff", [], [C], alpha)
    reactions = [R1, R2]
    
    # Create colonies for the simulation
    C1 = Colony("Test", 1000)
    colonies = [C1]

    gillespieSim = Gillespie(reactions, colonies)
    gillespieSim.run(timeLength)
    
    return gillespieSim.timeArray, gillespieSim.data

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
