import psutil
import numpy as np
import time
import Core

alpha = 0.01
omega = 0.2
muP = 0.2
p = 1.0
simLength = 100
numOfClones = 100
initIndex = 0

def virtual():
	f = psutil.virtual_memory().free/(1024*1024)
	u = psutil.virtual_memory().used/(1000000)
	return f

def swap():
	f = psutil.virtual_memory().free/(1000000)
	u = psutil.virtual_memory().used/(1000000)
	return f,u
init = virtual()
mem = virtual()
print "Started:", mem-init, "MB"
time.sleep(10)

xdata, ydata = Core.Simulation(alpha, omega, muP, p, simLength, numOfClones)
mem = virtual()
print "Created xdata, ydata:", mem-init, "MB"
init = virtual()
time.sleep(10)

zdata = np.zeros((len(ydata.keys()),len(ydata['P0'][initIndex:])))
for ind, key in enumerate(ydata.keys()):
    zdata[ind,:] = ydata[key][initIndex:]
mem = virtual()
print "Copied ydata to zdata:",mem-init, "MB"
init = virtual()
time.sleep(10)

del ydata
mem = virtual()
print "Deleted ydata",mem-init, "MB"
init = virtual()
time.sleep(5)

del zdata
mem = virtual()
print "Deleted zdata",mem-init, "MB"
init = virtual()
time.sleep(5)

del xdata
mem = virtual()
print "Deleted xdata",mem-init, "MB"
time.sleep(5)