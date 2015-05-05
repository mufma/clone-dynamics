import Core
import numpy as np


def cycle(alpha, omega, muP, p, simLength, numOfClones, initIndex):
	time, data = Core.Simulation(alpha, omega, muP, p,
                                 simLength,numOfClones)
	npData = np.zeros((len(data.keys()),len(data['P0'][initIndex:])))
    for ind, key in enumerate(data.keys()):
         npData[ind,:] = data[key][initIndex:]

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
	ydata = colnum

	del time

if __name__ == '__main__':
	alpha, omega, muP, p = 0.01, 0.2, 0.2, 1.0
	simLength = 100
	numOfClones = 10
	initIndex = 0
	cycle(alpha, omega, muP, p, simLength, numOfClones, initIndex)


