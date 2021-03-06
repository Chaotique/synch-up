"""

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
N_osc  = 25                                 # number of osci
spread = 1                                   # spread of osci distrib.
omg    = sort(spread*random.randn(N_osc))    # distribution of omg
                                             # randn: gauss, rand: iid,
                                             # standard_cauchy: lorentz
epsilon  = 1.85                              # coupling strength

# intergration parameter   
N_time = 10000                               # integration partition
tmax   = 1000.                               # time
y0     = (4*random.randn(N_osc))%(2.*pi)     # initial condition
t      = linspace(0, tmax, N_time)   

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





lin = phi_corr[100-1:]
omg_mean = 0 
for k in arange(len(lin)-1)+1:
    omg_mean = omg_mean + lin[k]/k

#phi_corr_fluct = lin + sum(lin)/len(lin)
#fft = fft.fft(phi_corr)



# plotting
scale = 0.15
#plt.figure(0)    
#plt.plot(t,y) 
#savepictopdfandtex('alltheta', filename1, plt, myfile, scale)

plt.figure(1)
plt.plot(order.real,order.imag)
plt.plot(order.real[0:20],order.imag[0:20])
plt.plot(order.real[N_time-20:N_time-1],order.imag[N_time-20:N_time-1])
plt.xlabel(r'$Re(R)$')
plt.ylabel(r'$Im(R)$')
plt.axis=([-1,1,-1,1])
plt.grid(True)
savepictopdfandtex('order', filename1, plt, myfile, scale)

plt.figure(2)
plt.plot(abs(order))
plt.xlabel('$t$')
plt.ylabel('norm of order parameter')
plt.grid(True)
savepictopdfandtex(r'$R$', filename1, plt, myfile, scale)

plt.figure(3)
#plt.plot(lin)
plt.plot(phi_corr)
plt.xlabel('$t$')
plt.ylabel('phase of order parameter')
plt.grid(True)
savepictopdfandtex('phase', filename1, plt, myfile, scale)

#plt.figure(4)
#plt.plot(fft)
#savepictopdfandtex('fft', filename1, plt, myfile, scale)

plt.figure(5)
plt.plot(omg)
plt.grid(True)
savepictopdfandtex('natfreq_spectrum', filename1, plt, myfile, scale)

plt.show()


# closing documentation with comment
enddoku(N_osc, spread, epsilon, N_time, tmax, myfile)
