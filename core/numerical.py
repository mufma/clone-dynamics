import numpy as np
import matplotlib.pyplot as plt

# Number of steps in simulation
steps = 100000

# Size of timestep
dt = 0.001

# Reactions parameters
p = 1.0
mu_p = 0.2
alpha = 0.01
omega = 0.2
mu_d = 0.2
K = 1000
C = 1000

# Upper limit of the clone size
N = 20

# Factorial of number
def factor(a, k):
    tot = 1
    for p in range(1,k+1):
        tot *= float(a+p)/p
    return tot

# Function to calculate equlibrium renew rate
def equilrate(alpha, p, mu_p, omega, K, C):
    mu = mu_p + omega
    return (p+mu)/2 - (p-mu)/2*np.sqrt(1 + (4*alpha*p*C)/(K*(p-mu)**2))

# Function to calculate number of clones
def numclones(alpha, p, mu_p, omega, K, C, k):
    mu = mu_p + omega
    r_eq = equilrate(alpha, p, mu_p, omega, K, C)
    r = r_eq/mu
    a = alpha/r_eq
    w = omega/mu_d
    return a*C*(r**k)*((1-r)**a)*factor(a,k)/(a+k)

#r_eq = equilrate(alpha,p,mu_p,omega,K,C)

# Array to store number of clones
clones = np.zeros((N,N))

# Assign equilibrium number of progenitor clones
for k in range(N):
    for n in range(N):
        if k == n:
            clones[k,n] = 10.0/np.log(n+2)
            #numclones(alpha, p, mu_p, omega, K, C, k)

# Record the number of clones at given step
clones_previous_step = clones.sum() - clones.sum(axis=0)[0]
print clones.sum(), clones_previous_step

# Change of number of clones in full equation
def deriv(p1, p2, p3, p4, p5, n1, n2, n3, n4, n5):
    return omega*(k+1)*p1 + (n+1)*mu_d*p2 + alpha*p3 + r_eq*(k-1)*p4 + mu_p*(k+1)*p5 - omega*k*n1 - n*mu_d*n2 - alpha*n3  - r_eq*k*n4 - mu_p*k*n5

for step in range(steps):
    # Save values at current step. Use copy to have independent arrays.
    copy_clones = np.copy(clones)
    c_k = copy_clones.sum(axis=1)
    k = range(N)
    N_p = (k*c_k).sum()
    r_eq = p*(1 - N_p/K)
    # Calculate new values using old values 
    for k in range(N):
        for n in range(N):
            y_kn = copy_clones[k,n]

            if (k==(N-1)) and (n!=(N-1)) and (n!=0):
                y_km1n = copy_clones[k-1,n]
                y_knp1 = copy_clones[k,n+1]
                clones[k,n] = y_kn + dt*deriv(0, y_knp1, y_km1n, y_km1n, 0, y_kn, y_kn, 0, 0, y_kn)
                
            elif (n==N-1) and (k!=0) and (k!=N-1):
                y_km1n = copy_clones[k-1,n]
                y_kp1nm1 = copy_clones[k+1,n-1]
                y_kp1n = copy_clones[k+1,n]
                clones[k,n] = y_kn + dt*deriv(y_kp1nm1, 0, y_km1n, y_km1n, y_kp1n, 0, y_kn, y_kn, y_kn, y_kn)
                
            elif (k==0) and (n!=0) and (n!=N-1):
                y_kp1nm1 = copy_clones[k+1,n-1]
                y_knp1 = copy_clones[k,n+1]
                y_kp1n = copy_clones[k+1,n]
                clones[k,n] = y_kn + dt*deriv(y_kp1nm1, y_knp1, 0, 0, y_kp1n, 0, y_kn, y_kn, y_kn, 0)
            
            elif (n==0) and (k!=0) and (k!=N-1):
                y_km1n = copy_clones[k-1,n]
                y_knp1 = copy_clones[k,n+1]
                y_kp1n = copy_clones[k+1,n]
                clones[k,n] = y_kn + dt*deriv(0, y_knp1, y_km1n, y_km1n, y_kp1n, y_kn, 0, y_kn, y_kn, y_kn)
            
            elif (k==0) and (n==0):
                y_knp1 = copy_clones[k,n+1]
                y_kp1n = copy_clones[k+1,n]
                clones[k,n] = y_kn + dt*deriv(0, y_knp1, 0, 0, y_kp1n, 0, 0, y_kn, 0, 0)
            
            elif (k==0) and (n==N-1):
                y_kp1nm1 = copy_clones[k+1,n-1]
                y_kp1n = copy_clones[k+1,n]
                clones[k,n] = y_kn + dt*deriv(y_kp1nm1, 0, 0, 0, y_kp1n, 0, y_kn, y_kn, 0, 0)

            elif (k==N-1) and (n==N-1):
                y_km1n = copy_clones[k-1,n]
                clones[k,n] = y_kn + dt*deriv(0, 0, y_km1n, y_km1n, 0, 0, y_kn, 0, 0, y_kn)
            
            elif (k==N-1) and (n==0):
                y_km1n = copy_clones[k-1,n]
                y_knp1 = copy_clones[k,n+1]
                clones[k,n] = y_kn + dt*deriv(0, y_knp1, y_km1n, y_km1n, 0, y_kn, 0, 0, 0, y_kn)

            else:
                y_km1n = copy_clones[k-1,n]
                y_knp1 = copy_clones[k,n+1]
                y_kp1n = copy_clones[k+1,n]
                y_kp1nm1 = copy_clones[k+1,n-1]
                clones[k,n] = y_kn + dt*deriv(y_kp1nm1, y_knp1, y_km1n, y_km1n, y_kp1n, y_kn, y_kn, y_kn, y_kn, y_kn)
    
    # Track the dynamics 
    if step%100==0:
        # Calculate total number of clones, even with 0 cells
        clones_total = clones.sum()
        # Calculate number of clones with at least 1 cell
        clones_current_step = clones_total - clones.sum(axis=0)[0]
        # Choose number of progenitor clones c_k for k=0,1
        progenitor_clones = clones.sum(axis=1)[0:2]
        print clones_current_step, clones_current_step-clones_previous_step, N_p
        clones_previous_step = clones_current_step
        
