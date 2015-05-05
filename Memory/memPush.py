import json
import psutil
import time
import numpy as np

def virtual():
	f = psutil.virtual_memory().free/(1024*1024)
	return f


"""
time.sleep(5)
outfile = open('output','w')

for i in range(5):
	x = np.linspace(0,1,1000000)
	json.dump(x, outfile)
"""



mem = virtual()
print "Started:", mem, "MB"
x = np.linspace(0,1,10000000)
time.sleep(10)
mem = virtual()
print "x = linspace:", mem, "MB"
del x
time.sleep(10)
mem = virtual()
print "del x:", mem, "MB"
x = 0
time.sleep(10)
mem = virtual()
print "x = 0:", mem, "MB"





