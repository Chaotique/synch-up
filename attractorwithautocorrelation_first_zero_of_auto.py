"""
Finite size effects in a Kuramoto model with natural frequencies omg, 
global identical coupling epsilon, noise free (except the finite size noise)

here: starting from different initial conditions, time evolution with either 
gaussian distributed or equidistant natural frequencies

plots:




"""

# public modules
from numpy import *
import cmath as cm
from matplotlib import pyplot as plt
import os
from scipy.integrate import odeint
import time  

# proper modules
from integratordocumentation import dokufile, enddoku, savepictopdfandtex

def func(y, t, N_osc, omg, epsilon):
    """ Kuramoto model with natural frequencies omg, 
    global identical coupling epsilon, 
    N_osc oscillators, y[k] == \theta_k
    \dot\theta_k=\omega_k+\frac{\epsilon}{N}\sum_{j=1}^N\sin(\theta_j-\theta_k)
    """
    y_help = zeros((N_osc))            # sum over sines
    for i in arange(N_osc):            
        y_help[i] = sum(sin(y-y[i]))
    return (omg + epsilon*y_help/N_osc)
    

# system parameter
N_osc  = 500#00                              # number of osci
spread = 1.                                   # spread of osci distrib.

epsilon  = 1.85                              # coupling strength

# intergration parameter   
N_time = 100000                             # integration partition
tmax   = 1000.                               # time

t      = linspace(0, tmax, N_time)   


omg    = linspace(-spread,spread,N_osc)    #   # distribution of omg
omg = sort(spread*random.randn(N_osc))
meanomg = mean(omg)
print meanomg


# randn: gauss, rand: iid,
# standard_cauchy: lorentz
y0     = (0.05*(random.rand(N_osc))+linspace(0,2*pi,num = N_osc, endpoint = False))%(2.*pi)     # initial condition
y      = odeint(func, y0, t, (N_osc, omg, epsilon))%(2*pi) # integration


# documentation
myfile = open("../pics_zu_github/" + os.path.basename(__file__) + ".tex", "a+b")
filename1 = dokufile(myfile)


# order parameter, phase
order  = ones(N_time)+1j*ones(N_time)      # R*exp(i phi)
phi    = ones(N_time)                      # phi

# glue the phase together every 2pi to get a continuous function in time
phi_corr = ones(N_time)                    # continuous extension of phi
phase2pi = 0                               # cumulating phasees 2pi
for i in arange(N_time):
    order[i] = sum(cos(y[i])+1j*sin(y[i]))/N_osc
    phi[i] = cm.phase(order[i])
    if (phi[i]-phi[i-1])>(pi):
        phase2pi = phase2pi - 2.*pi   
    if (-phi[i]+phi[i-1])>(pi):
        phase2pi = phase2pi + 2.*pi
    phi_corr[i] = phi[i] + phase2pi


#autocorrelation of the phase
meanvelo = (phi_corr[N_time-1]-phi_corr[100])*100/(N_time-1-100)
N_tau = 1000
auto = zeros(N_tau)
for tau in arange(N_tau):
    auto[tau] = sum((phi_corr[100:N_time-N_tau-1]-meanvelo*t[100:N_time-N_tau-1])*(phi_corr[100+tau:N_time-N_tau-1+tau]-meanvelo*t[100+tau:N_time-N_tau-1+tau]))/(N_time-N_tau-100)
    


# plotting
scale = 0.15


plt.figure(1)
plt.plot(order.real,order.imag)#, 'o')
plt.plot(order.real[0:20],order.imag[0:20])#, 'o')
plt.plot(order.real[N_time-20:N_time-1],order.imag[N_time-20:N_time-1])#, 'o')
plt.xlabel(r'$Re(R)$')
plt.ylabel(r'$Im(R)$')
plt.axis=([-1,1,-1,1])
plt.grid(True)
savepictopdfandtex('order', filename1, plt, myfile, scale)


plt.figure(3)
#plt.plot(lin)
plt.plot(phi_corr)
plt.plot(phi_corr-meanvelo*t)
#plt.plot(meanomg*t, 'g')
plt.xlabel('$t$')
plt.ylabel('phase of order parameter')
#Rmean = mean(R[200:N_time-1])
#meanvelocity = meanomg/Rmean
#plt.plot(meanomg/R*t,'b--')
plt.grid(True)
savepictopdfandtex('phase', filename1, plt, myfile, scale)


plt.figure(4, figsize=(24,12))
plt.title('attractor of global phase velocity with delay ')
for delay in arange(10)*1:
    # attractor plotting
    #delay = 3
    d = delay/1
    plt.subplot(2,5,repr(d))
    global_phase_velocity = phi_corr[1:]-phi_corr[:-1]
    attractor = global_phase_velocity[200:-300]
    attractordelay = global_phase_velocity[200+delay:-300+delay]
    plt.plot(attractor, attractordelay)#, '.', markersize = 0.8)
    plt.xlabel('global phase'+r'$(t)$')
    plt.ylabel('global phase'+r'$(t+'+repr(delay)+')$')
    plt.axis=([-1,1,-1,1])#plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True)
savepictopdfandtex('attractorphasevelo', filename1, plt, myfile, scale)

plt.figure(5, figsize=(24,12))
plt.title('attractor of global phase velocity with larger delay ')
for delay in (arange(10)+10)*1:
    # attractor plotting
    #delay = 3
    d = delay/1-10
    plt.subplot(2,5,repr(d))
    global_phase_velocity = phi_corr[1:]-phi_corr[:-1]
    attractor = global_phase_velocity[200:-300]
    attractordelay = global_phase_velocity[200+delay:-300+delay]
    plt.plot(attractor, attractordelay)#, '.', markersize = 0.8)
    plt.xlabel('global phase'+r'$(t)$')
    plt.ylabel('global phase'+r'$(t+'+repr(delay)+')$')
    plt.axis=([-1,1,-1,1])#plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True)
    savepictopdfandtex('attractorphasevelo', filename1, plt, myfile, scale)


plt.figure(6)
plt.plot(auto)
plt.xlabel('$t$')
plt.ylabel('autocorrelation of the phase of the order parameter')
plt.grid(True)
savepictopdfandtex('autophase', filename1, plt, myfile, scale)
plt.show()
# closing documentation with comment
enddoku(N_osc, spread, epsilon, N_time, tmax, myfile)
