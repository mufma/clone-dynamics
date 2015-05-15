import psutil
import copy
import time

def virtual():
	f = psutil.virtual_memory().free/(1024*1024)
	return f


init = psutil.virtual_memory().free/(1024*1024)
x=range(1000000) # allocate a big list
time.sleep(5)
mem = psutil.virtual_memory().free/(1024*1024)
print "x=range:",init-mem,"MB"
init = mem
y=copy.deepcopy(x)
time.sleep(5)
mem = psutil.virtual_memory().free/(1024*1024)
print "y=copy:",init-mem,"MB"
init = mem
del x
time.sleep(5)
mem = psutil.virtual_memory().free/(1024*1024)
print "del x:",init-mem,"MB"
init = mem
del y
time.sleep(5)
mem = psutil.virtual_memory().free/(1024*1024)
print "del y:",init-mem,"MB"

