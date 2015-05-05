# -*- coding: utf-8 -*-
"""
Created on Sun Dec 21 00:15:09 2014

@author: maratmufteev
"""
import Core
import time

alpha = 0.01
omega = 0.48
muP = 0.48
r = 1.0
length = 250
numColonies = 10

TEST = False
if TEST == True:
    Core.PropensityTestCase()
    Core.UpdateDecreaseTestCase()
    Core.UpdateIncreaseTestCase()
    Core.UpdateEmptyDecreaseTestCase()
    Core.UpdateEmptyIncreaseTestCase()
    Core.DataStoreTestCase()

time, data = Core.SaturationTestCase(alpha, omega, muP, r, length, numColonies)
for key in data:
    plt.plot(time, data[key], '--')
plt.show()

def AlgoTiming():
    timeDiff = []
    numArray = [10,100,200,300]
    for numColonies in numArray:
        init = time.time()
        Core.Simulation(alpha, omega, muP, r, length, numColonies)
        end = time.time()
        timeDiff.append(end-init)

    plt.plot(numArray, timeDiff, 'r--')
    plt.plot(numArray, timeDiff, 'b.')
    plt.show()








