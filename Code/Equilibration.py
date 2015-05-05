# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 23:29:56 2014

@author: maratmufteev
"""

import Core
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

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
omega = 0.4
muP = 0.4
p = 1.0
length = 100
numOfClones = 1000
# You can change it in Core.py
boneCapacity = 1000

legClones = []
legCells = []
legName = [r'$\alpha$=0.01',r'$\alpha$=0.05',r'$\alpha$=0.1']
for alpha in [0.01, 0.05, 0.1]:
    
    steadyCells = calculateSteadyCells(alpha, omega, muP, p, 
                                       numOfClones, boneCapacity)
    steadyClones = calculateSteadyClones(alpha, omega, muP, p, 
                                         numOfClones, boneCapacity)

    print "alpha = ", alpha
    time, data = Core.Simulation(alpha, omega, muP, p, length, numOfClones)
    
    dataList = []
    for key in data.keys():
        dataList.append(data[key])
    npData = np.array(dataList)
    
    del dataList
    del data
    
    total = np.zeros((len(npData[0,:]),1))
    colnum = np.zeros((len(npData[0,:]),1))
    for ind in range(len(npData[0,:])):
        total[ind] = npData[:,ind].sum()
        colnum[ind] = len((npData[:,ind])[npData[:,ind]!=0])
    
    del npData

    plt.figure()
    plt.plot(time, total)
    plt.title(r'$\alpha$ = {0} $\mu$+$\omega$ = {1} $p$ = {2}'.format(alpha, 
                  muP + omega, p))
    plt.xlabel("Simulation time \n\n" + "Total number of colonies = {0}".format(numOfClones)
                + "\n Bone capacity: {0}".format(boneCapacity))
    plt.ylabel("Total number of cells")
    plt.axhline(y=steadyCells, c='g', linestyle='--')
    plt.gcf().subplots_adjust(bottom=0.22)
    plt.savefig("TotalNumCells_alpha{0}_p{1}_mu{2}_boneCap{3}.png".format(alpha, p, muP+omega,
                boneCapacity))   
    
    plt.figure()
    plt.plot(time, colnum)
    plt.title(r'$\alpha$ = {0} $\mu$+$\omega$ = {1} $p$ = {2}'.format(alpha, 
                  muP + omega, p))
    plt.xlabel("Simulation time \n\n" + "Total number of colonies = {0}".format(numOfClones)
                + "\n Bone capacity: {0}".format(boneCapacity))
    plt.ylabel("Number of clones")
    plt.axhline(y=steadyClones, c='g', linestyle='--')
    plt.gcf().subplots_adjust(bottom=0.22)
    plt.savefig("NumberClones_alpha{0}_p{1}_mu{2}_boneCap{3}.png".format(alpha, p, muP+omega,
                boneCapacity))
    
    plt.figure("JointClones")
    leg, = plt.plot(time, colnum)
    plt.title(r'$\mu$ = {0} $p$ = {1}'.format(muP + omega, 
              p))
    plt.xlabel("Simulation time \n\n" + "Total number of colonies = {0}".format(numOfClones)
                + "\n Bone capacity: {0}".format(boneCapacity))
    plt.ylabel("Number of clones")
    plt.axhline(y=steadyClones, c='g', linestyle='--')
    legClones.append(leg)

    plt.figure("JointCells")
    leg, = plt.plot(time, total)
    plt.title(r'$\mu$ = {0} $p$ = {1}'.format(muP + omega, 
              p))
    plt.xlabel("Simulation time \n\n" + "Total number of colonies = {0}".format(numOfClones)
                + "\n Bone capacity: {0}".format(boneCapacity))
    plt.ylabel("Number of cells")
    plt.axhline(y=steadyCells, c='g', linestyle='--')
    legCells.append(leg)
    
    del colnum
    del total
    del time

plt.figure("JointClones")
plt.legend(legClones, legName)
plt.savefig("JointTotalNumCells_mu{0}_p{1}_boneCap{2}.png".format(muP+omega, p, boneCapacity))


plt.figure("JointCells")
plt.legend(legCells, legName)
plt.savefig("JointNumberClones_mu{0}_r{1}_boneCap{2}.png".format(muP+omega, p, boneCapacity))
