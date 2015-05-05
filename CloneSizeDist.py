# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 23:33:18 2014

@author: maratmufteev
"""
import Core
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

alpha = 0.1
omega = 0.2
muP = 0.2
r = 1.0
length = 10
numColonies = 10
# You can change it in Core.py
boneCap = 1000

for muP in [0.1, 0.2, 0.4]:
    print "muP:",muP
    omega = muP
    time, data = Core.Simulation(alpha, omega, muP, r, length, numColonies)
    dataList = []
    for key in data.keys():
        dataList.append(data[key])
    npData = np.array(dataList)
    n = len(npData[0,:])
    
    plt.figure()
    plt.hist(npData[:,0], range=[0.1, 30.0], histtype = 'stepfilled')
    plt.title(r'$\alpha$ = {0} $\mu$+$\omega$ = {1} $r$ = {2}'.format(alpha, 
                  muP + omega, r))
    plt.ylabel("Number of clones")
    plt.xlabel("Clone size \n\n" + "Total number of colonies = {0}".format(numColonies)
                + "\n Time: {0:.3}".format(0.) + "\n Bone capacity: {0}".format(boneCap))
    plt.gcf().subplots_adjust(bottom=0.22)
    plt.savefig("CloneSizeDist_alpha{0}_r{1}_mu{2}_time{3:.3}_boneCap{4}.png".format(alpha, r, muP+omega,
                0., boneCap))
    
    plt.figure()
    plt.hist(npData[:,n/2], range=[0.1, 30.0], histtype = 'stepfilled')
    plt.title(r'$\alpha$ = {0} $\mu$+$\omega$ = {1} $r$ = {2}'.format(alpha, 
                  muP + omega, r))
    plt.ylabel("Number of clones")
    plt.xlabel("Clone size \n\n" + "Total number of colonies = {0}".format(numColonies)
                + "\n Time: {0:.3}".format(time[n/2])+ "\n Bone capacity: {0}".format(boneCap))
    plt.gcf().subplots_adjust(bottom=0.22)
    plt.savefig("CloneSizeDist_alpha{0}_r{1}_mu{2}_time{3:.3}_boneCap{4}.png".format(alpha, r, muP+omega,
                time[n/2], boneCap))

    
    plt.figure()
    plt.hist(npData[:,n-1], range=[0.1, 30.0], histtype = 'stepfilled')
    plt.title(r'$\alpha$ = {0} $\mu$+$\omega$ = {1} $r$ = {2}'.format(alpha, 
                  muP + omega, r))
    plt.ylabel("Number of clones")
    plt.xlabel("Clone size \n\n" + "Total number of colonies = {0}".format(numColonies)
                + "\n Time: {0:.3}".format(time[n-1])+ "\n Bone capacity: {0}".format(boneCap))
    plt.gcf().subplots_adjust(bottom=0.22)
    plt.savefig("CloneSizeDist_alpha{0}_r{1}_mu{2}_time{3:.3}_boneCap{4}.png".format(alpha, r, muP+omega,
                time[n-1], boneCap))
    
    plt.figure()
    plt.hist(npData[:,n/2], range=[0.1, 30.0], histtype = 'stepfilled')
    plt.hist(npData[:,n-1], range=[0.1, 30.0], histtype = 'stepfilled', alpha = 0.8)
    plt.title(r'$\alpha$ = {0} $\mu$+$\omega$ = {1} $r$ = {2}'.format(alpha, 
                  muP + omega, r))
    plt.ylabel("Number of clones")
    plt.xlabel("Clone size \n\n" + "Total number of colonies = {0}".format(numColonies)
                + "\n Bone capacity: {0}".format(boneCap))
    plt.gcf().subplots_adjust(bottom=0.22)
    plt.savefig("JointCloneSize_alpha{0}_r{1}_mu{2}_boneCap{3}.png".format(alpha, r, muP+omega,
                boneCap))
    
    extData = extinctionTime(data)
    plt.figure()
    npTime = np.array(time)
    histDat = npTime[extData]
    plt.hist(histDat, histtype = 'stepfilled')
    plt.title(r'$\alpha$ = {0} $\mu$+$\omega$ = {1} $r$ = {2}'.format(alpha, 
                  muP + omega, r))
    plt.ylabel("Number of clones")
    plt.xlabel("Extinction time \n\n" + "Total number of colonies = {0}".format(numColonies)
                + "\n Bone capacity: {0}".format(boneCap))
    plt.gcf().subplots_adjust(bottom=0.22)
    plt.savefig("ExtinctionTime_alpha{0}_r{1}_mu{2}_boneCap{3}.png".format(alpha, r, muP+omega,
                boneCap))      
            
# USE FOR LOG SCALE PLOTS
# plt.yscale('log', nonposy='clip')