# -*- coding: utf-8 -*-
"""
Created on Fri Dec 19 02:14:18 2014

@author: maratmufteev
"""
import Core
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def plotColonies(time, data, alpha, omega, muP, r, length, numColonies):
    plt.figure()
    colors = [cm.jet(ind) for ind in np.linspace(0, 1, len(data))]
    for ind, col in enumerate(data):
        plt.plot(time, data[col], color = colors[ind], linestyle = '--', 
                 alpha = 0.8)
        plt.title(r'$\alpha$ = {0} $\mu$+$\omega$ = {1} $r$ = {2}'.format(alpha, 
                  muP + omega, r))
        plt.ylabel("Number of cells")
        plt.xlabel("Time \n\n" + "Total number of colonies = {0}".format(numColonies))
        plt.gcf().subplots_adjust(bottom=0.15)
        plt.savefig("Dynamics_alpha{0}_r{1}_mu{2}.png".format(alpha, r, muP+omega))
    plt.show()

def extinctionTime(data):
    dataList = []
    for key in data.keys():
        dataList.append(data[key])    
    
    extinction = []
    for colData in dataList:
        zerosInd = [ind for ind, colSize in enumerate(colData) if colSize == 0]
        try:
            extinction.append(zerosInd[0])
        except:
            pass
    return extinction

def calculateSteadyCells(alpha, omega, muP, p, numOfClones, boneCapacity):
    mu = muP + omega
    C = numOfClones
    K = boneCapacity
    a = alpha
    w = omega
    part1 = K*(p-mu)/(2*p)
    part2 = 1 + np.sqrt(1 + 4*a*p*C/(K*(p-mu)**2))
    
    return part1*part2

def calculateSteadyRenew(alpha, omega, muP, p, numOfClones, boneCapacity):
    mu = muP + omega
    C = numOfClones
    K = boneCapacity
    a = alpha
    part1 = (p+mu)/2
    part2 = (p-mu)*(np.sqrt(1 + 4*a*p*C/(K*(p-mu)**2)))/2
    
    return part1 - part2
    
def calculateSteadyClones(alpha, omega, muP, p, numOfClones, boneCapacity):
    mu = muP + omega
    C = numOfClones
    K = boneCapacity
    rSteady = calculateSteadyRenew(alpha, omega, muP, p, numOfClones, boneCapacity)
    r = rSteady/mu
    a = alpha/rSteady
    
    return C*(1 - (1 - r)**a)

alpha = 0.01
omega = 0.1
muP = 0.1
p = 1.0
simLength = 100
numOfClones = 1000
# You can change it in Core.py
boneCapacity = 1000

print "alpha:", alpha
print "p:", p
print "mu:", muP+omega
print "Steady Number of Cells:", calculateSteadyCells(alpha, omega, muP, p, numOfClones, boneCapacity)
print "Steady Number of Clones:", calculateSteadyClones(alpha, omega, muP, p, numOfClones, boneCapacity)

"""
for cloneData in dataList:

    zero = [ind for ind, el in enumerate(cloneData) if el == 0]
    posit = [ind for ind, el in enumerate(cloneData) if el != 0]
    zeroSep = [[zero[0]]]
    track = 0
    for ind in range(1,len(zero)):
        if zero[ind] - zero[ind-1] == 1:
            zeroSep[track].append(zero[ind])
        else:
            track += 1
            zeroSep.append([])
            zeroSep[track].append(zero[ind])
    posSep = [[posit[0]]]
    track = 0
    for ind in range(1,len(posit)):
        if posit[ind] - posit[ind-1] == 1:
            posSep[track].append(posit[ind])
        else:
            track += 1
            posSep.append([])
            posSep[track].append(posit[ind])

    maxEl
    for el in range(len(posSep)):
        maxEl.append((np.array(cloneData))[posSep[el]].max())
"""

"""
for colData in dataList:
    largeInd = [ind for ind, colSize in enumerate(colData) if colSize == 0]
    try:
        if largeInd[0] > 10000:
            plt.figure(1)
            plt.plot(colData)
        if largeInd[0] < 500:
            plt.figure(2)
            plt.plot(colData)
    except:
        pass
"""

"""
plt.figure()
time, data = Core.Simulation(alpha, omega, muP, r, length, numColonies)
colors = [cm.jet(ind) for ind in np.linspace(0, 1, len(data))]
for ind, col in enumerate(data):
    plt.plot(time, data[col], color = colors[ind], linestyle = '--', 
             alpha = 0.8)
"""







