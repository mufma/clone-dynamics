import numpy as np
import json

def convert_to_numpy(file):
    """
    Convert data from file to numpy array.
    
    Variables type:
    file - txt file
    
    Output type:
    collector - numpy 2-D array
    
    Details about data in txt file:
    - Results of simulation appears as dictionary like below
    >> data = {'cell 1': [1,2,3], 'cell 2': [2,1,5]}
    - dumps function from json library produces a string
    >> jsondata = json.dumps(data)
    >> jsondata
    >> "{'cell 1': [1,2,3], 'cell 2': [2,1,5]}"
    - we save string in txt file using
    >> with open("output.txt", "w") as text_file:
	       text_file.write(jsondata)
	  
	Usage example:
	>> npdata = convert_to_numpy("output.txt")
	>> npdata
	>> array([[1,2,3],[2,1,5]])
    """
    with open(file, "r") as text_file:
	    jsondata = text_file.read()
    data = json.loads(jsondata)
    
    firstkey = data.keys()[0]
    collector = np.array(data[firstkey])
    for key in data.keys()[1:]:
        collector = np.vstack((collector, np.array(data[key])))
    return collector

def count_clones(data):
    """
    Count number of alive(cellcount > 0) clones at each timestep.
    
    Variables type:
    data - numpy array
    
    Output type:
    numpy 1-D array
    
    Details about data:
    data stores information about colonies in format
            time: 0     time: 1     time: 2 ...    
    
    clone 1   23          23          24
    
    clone 2   45          44          44
    
    using numpy array
    >> data
    [[2, 1, 1, 0, 0],
     [0, 0, 1, 1, 0]]
     
    Usage example:
    >> data
    [[2,1,1,0,0],
     [0,0,1,1,0]]
    >> count_clones(data)
    [1,1,2,1,0]
    """
    count = []
    print "Shape of data array:", np.shape(data)
    for ind in range(np.shape(data)[1]):
        count.append(np.count_nonzero(data[:,ind]))
    return np.array(count)

def steady_total_progenitors(alpha, omega, mup, p, num_of_clones, bone_capacity):
    """
    Calculate total number of progenitor cells in equilibrium.
    
    Variable types:
    alpha - float
    omega - float
    mup - float
    p - float
    num_of_clones - integer/float
    bone_capacity - integer/float
    """
    mu = mup + omega
    C = num_of_clones
    K = bone_capacity
    a = alpha
    w = omega
    part1 = K*(p-mu)/(2*p)
    part2 = 1 + np.sqrt(1 + 4*a*p*C/(K*(p-mu)**2))
    
    return part1*part2

def steady_renew_rate(alpha, omega, mup, p, num_of_clones, bone_capacity):
    """
    Calculate renew rate of progenitor cells in steady state.
    
    Variable types:
    alpha - float
    omega - float
    mup - float
    p - float
    num_of_clones - integer/float
    bone_capacity - integer/float
    """
    mu = mup + omega
    C = num_of_clones
    K = bone_capacity
    a = alpha
    part1 = (p+mu)/2
    part2 = (p-mu)*(np.sqrt(1 + 4*a*p*C/(K*(p-mu)**2)))/2
    
    return part1 - part2
    
def steady_clones_progenitors(alpha, omega, mup, p, num_of_clones, bone_capacity):
    """
    Calculate number of alive(cell count > 0) progenitors clones in steady state.
    
    Variable types:
    alpha - float
    omega - float
    mup - float
    p - float
    num_of_clones - integer/float
    bone_capacity - integer/float
    """
    mu = mup + omega
    C = num_of_clones
    r_steady = steady_renew_rate(alpha, omega, mup, p, num_of_clones, bone_capacity)
    r = r_steady/mu
    a = alpha/r_steady
    
    return C*(1 - (1 - r)**a)

def steady_clones_mature(alpha, omega, mup, p, mum, num_of_clones, bone_capacity):
    """
    Calculate number of alive(cell count > 0) mature clones in steady state.
    
    Variable types:
    alpha - float
    omega - float
    mup - float
    p - float
    num_of_clones - integer/float
    bone_capacity - integer/float
    """
    mu = mup + omega
    C = num_of_clones
    r_steady = steady_renew_rate(alpha, omega, mup, p, num_of_clones, bone_capacity)
    r = r_steady/mu
    a = alpha/r_steady
    w = omega/mum

    top = 1.0 - r
    low = 1.0 - r*np.exp(-w)

    return C*(1 - (top/low)**a)







