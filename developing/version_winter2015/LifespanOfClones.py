# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 22:20:46 2014

@author: maratmufteev
"""
import Core
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def groupIndicies(indOfPositiveSize):
    positiveIntervals = [[indOfPositiveSize[0]]]
    intervalNumber = 0
    for num in range(1,len(indOfPositiveSize)):
        if indOfPositiveSize[num] - indOfPositiveSize[num-1] == 1:
            positiveIntervals[intervalNumber].append(indOfPositiveSize[num])
        else:
            intervalNumber += 1
            positiveIntervals.append([])
            positiveIntervals[intervalNumber].append(indOfPositiveSize[num])

    intervalGroup = np.zeros(len(positiveIntervals))
    for ind, interval in enumerate(positiveIntervals):
        intervalGroup[ind] = len(interval)
    return intervalGroup

alpha = 0.01
omega = 0.1
muP = 0.1
p = 1.0
simLength = 100
numOfClones = 1000
# You can change it in Core.py
boneCapacity = 1000

time, clonesDynamics = Core.Simulation(alpha, omega, muP, p, simLength, numOfClones)
cloneGroup = []
for cloneName in clonesDynamics.keys():
    cloneGroup.append(clonesDynamics[cloneName])

del clonesDynamics

for sizesOfClone in cloneGroup:
    #zero = [ind for ind, elem in enumerate(sizesOfClone) if elem == 0]
    indOfPositiveSize = [ind for ind, size in enumerate(sizesOfClone) if size > 0]

    """
    zeroSep = [[zero[0]]]
    intervalNumber = 0
    for ind in range(1,len(zero)):
        if zero[ind] - zero[ind-1] == 1:
            zeroSep[intervalNumber].append(zero[ind])
        else:
            intervalNumber += 1
            zeroSep.append([])
            zeroSep[intervalNumber].append(zero[ind])
    """

    if len(indOfPositiveSize)>0:
        intervalGroup = groupIndicies(indOfPositiveSize)

        intervalMaxGroup = [20000,30000]
        for figNumber, maxInterval in enumerate(intervalMaxGroup):
            if np.array(intervalGroup).min()>maxInterval:
                plt.figure(figNumber)
                plt.title("Long-lived colonies")
                plt.xlabel("Time \n" + "Lifespan greater than: {0}".format(time[maxInterval]))
                plt.ylabel("Colony size")
                plt.gcf().subplots_adjust(bottom=0.15)
                plt.plot(time,sizesOfClone)
        passFigNumber = len(intervalMaxGroup)     


        intervalMinGroup = [5000]
        for figNumber, minInterval in enumerate(intervalMinGroup):
            if np.array(intervalGroup).max()<minInterval:
                plt.figure(figNumber + passFigNumber)
                plt.title("Short-lived colonies")
                plt.xlabel("Time \n" + "Lifespan smaller than: {0}".format(time[minInterval]))
                plt.ylabel("Colony size")
                plt.gcf().subplots_adjust(bottom=0.15)
                plt.plot(time,sizesOfClone)     

plt.show()