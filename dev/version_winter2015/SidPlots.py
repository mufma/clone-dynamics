# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 18:49:32 2015

@author: maratmufteev
"""
import Core
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def plotColonies(time, data, alpha, omega, muP, p, simLength, numColonies):
    plt.figure()
    colors = [cm.jet(ind) for ind in np.linspace(0, 1, len(data))]   
    for ind, col in enumerate(data):
        plt.plot(time, data[col], color = colors[ind], linestyle = '--', 
                 alpha = 0.8)
    plt.title(r'$\alpha$ = {0} $\mu$+$\omega$ = {1} $p$ = {2}'.format(alpha, 
                  muP + omega, p))
    plt.xticks(np.linspace(min(time), max(time), 4, dtype=int))
    plt.xlim(0,max(time))
    plt.locator_params(axis='y', nbins=4)
    plt.savefig("Dynamics_alpha{0}_p{1}_mu{2}.png".format(alpha, p, muP+omega))

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

# Parameters
alpha = 0.01
omega = 0.2
muP = 0.2
p = 1.0
simLength = 100
numOfClones = 1000
boneCapacity = 1000 # You can change it in Core.py

"""
for alpha in [0.01]:
	for muP in [0.1]:
		omega = muP
		print "alpha:", alpha, "\n" 
		print "mu:", muP+omega

		time, data = Core.Simulation(alpha, omega, muP, p, simLength, numOfClones)
		print "Finished simulation"
        plotColonies(time, data, alpha, omega, muP, p, simLength, numOfClones)



legCells = []
legName = [r'$\alpha$=0.01',r'$\alpha$=0.05',r'$\alpha$=0.1']
for alpha in [0.01, 0.05, 0.1]:
    
    steadyCells = calculateSteadyCells(alpha, omega, muP, p, 
                                       numOfClones, boneCapacity)

    print "alpha = ", alpha
    time, data = Core.Simulation(alpha, omega, muP, p, simLength, numOfClones)
    
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
        
    plt.figure("JointCells")
    leg, = plt.plot(time, total)
    plt.title(r'$\mu$ = {0} $p$ = {1}'.format(muP + omega, 
              p))
    plt.axhline(y=steadyCells, c='g', linestyle='--')
    legCells.append(leg)
    
    del total

fig = plt.figure("JointCells")
ax = fig.get_axes()
info = plt.setp(ax, xticks=np.linspace(min(time), max(time), 4, dtype=int), 
                yticks=np.linspace(0, int(round(1.2*steadyCells,-2)), 5, dtype=int))
plt.legend(legCells, legName, fontsize=20)

#plt.savefig("JointTotalNumCells_mu{0}_p{1}_boneCap{2}.png".format(muP+omega, p, boneCapacity))

"""
cloneStat = []
for alpha in [0.01, 0.03, 0.05, 0.07, 0.1]:
    cloneStat.append([])
    print "alpha = ", alpha
    for rep in [1,2,3]:
        print "repetition = ", rep
        time, data = Core.Simulation(alpha, omega, muP, p, simLength, numOfClones)
        
        dataList = []
        for key in data.keys():
            dataList.append(data[key])
        npData = np.array(dataList)
        
        del dataList
        del data

        colnum = np.zeros((len(npData[0,:]),1))
        for ind in range(len(npData[0,:])):
            colnum[ind] = len((npData[:,ind])[npData[:,ind]!=0])
        
        del npData
        
        cloneStat[len(cloneStat)-1].append(np.array(colnum[20000:]).mean())

params = np.linspace(0, 0.11, 200)
predictedClones = calculateSteadyClones(params, omega, muP, p, numOfClones, boneCapacity)        
        
cloneStat = np.array(cloneStat)
plt.errorbar([0.01, 0.03, 0.05, 0.07, 0.1], cloneStat.mean(axis=1),
             yerr = cloneStat.std(axis=1), ecolor='g', capthick=1.5, fmt='o')
plt.plot(params, predictedClones)
plt.title(r'$\mu$ = {0} $p$ = {1}'.format(muP + omega, p))





















   
        