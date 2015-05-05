# -*- coding: utf-8 -*-
"""
Created on Fri Dec 26 14:26:32 2014

@author: maratmufteev
"""

import Core
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import scipy.optimize as optimization

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

def func(x, a, b, c):
    return a + b*x + c*x*x

alpha = 0.01
omega = 0.2
muP = 0.2
p = 1.0
simLength = 10
numOfClones = 10
# You can change it in Core.py
boneCapacity = 1000
initIndex = 0
#30000

for alpha in [0.01]:
	for muP in [0.1]:
		omega = muP
		print "alpha:", alpha, "\n" 
		print "mu:", muP+omega

		time, data = Core.Simulation(alpha, omega, muP, p, simLength, numOfClones)
		print "Finished simulation"

		dataList = []
		for key in data.keys():
		    dataList.append(data[key][initIndex:])
		npData = np.array(dataList)

		del dataList
		del data

		total = np.zeros(len(npData[0,:]))
		colnum = np.zeros(len(npData[0,:]))
		for ind in range(len(npData[0,:])):
		    total[ind] = npData[:,ind].sum()
		    colnum[ind] = len((npData[:,ind])[npData[:,ind]!=0])

		del npData

		# Generate artificial data = straight line with a=0 and b=1
		# plus some noise.
		xdata = np.array(time[initIndex:])
		ydata = total

		del time

		meanNumber = total.mean()
		stdNumber = total.std()
		steadyCells = calculateSteadyCells(alpha, omega, muP, p, 
		                                   numOfClones, boneCapacity)

		plt.figure()

		output = plt.hist(total, bins=50, histtype='stepfilled', alpha=0.8)

		"""
		hist, bin_edges = np.histogram(total, bins = 50) 
		centers = (bin_edges[1:] + bin_edges[:-1])/2.
		plt.stem(centers, hist, linefmt='b-', markerfmt='bo', basefmt='r-')
		"""

		plt.xlabel("Number of cells\n\n" + r'$\alpha$=%.2f $\mu$=%.2f $\mathrm{p}$=%.2f'%(alpha, muP + omega, p))
		plt.ylabel("Counts")
		plt.title("Distribution of total number of cells")
		plt.gcf().subplots_adjust(bottom=0.18)

		plt.axvline(x=meanNumber,c='r',linewidth=2,linestyle='--', label='Mean Number=%.2f'%meanNumber)
		plt.axvspan(meanNumber-stdNumber,meanNumber+stdNumber,color = 'r',alpha=0.3)
		plt.axvline(x=steadyCells, c='g', linewidth=2,linestyle='--', label='Steady Number=%.2f'%steadyCells)

		plt.legend(loc=2)
		plt.savefig("HistCellCounts_alpha{0}_p{1}_mu{2}_boneCap{3}.png".format(alpha, p, muP+omega,
		                boneCapacity)) 



		parameters, covariance = optimization.curve_fit(func, xdata, ydata)

		plt.figure(figsize=(9,7))
		plt.plot(xdata, ydata, 'r.')
		plt.plot(xdata, func(xdata, parameters[0], parameters[1], parameters[2]), label='fitting')
		plt.xlabel("Time\n Fitting data to:" + '$\mathit{a}+\mathit{b}x+\mathit{c}x^{2}$\n' + 
					'$\mathit{a}$=%.1f $\pm$ %.1f '%(parameters[0],covariance[0][0]) + '\n' +
					'$\mathit{b}$=%.3f $\pm$ %.3f '%(parameters[1],covariance[1][1]) + '\n' +
					'$\mathit{c}$=%.7f $\pm$ %.7f '%(parameters[2],covariance[2][2]) + '\n')
		plt.ylabel("Number of cells")
		plt.title(r'$\alpha$=%.2f $\mu$=%.2f $\mathrm{p}$=%.2f'%(alpha, muP + omega, p))
		plt.axhline(y=steadyCells, c='g', linestyle='--', label='steady state')
		plt.gcf().subplots_adjust(bottom=0.2)
		plt.legend()
		plt.savefig("FittingMean_alpha{0}_p{1}_mu{2}_boneCap{3}.png".format(alpha, p, muP+omega,
		                boneCapacity)) 
plt.show()


