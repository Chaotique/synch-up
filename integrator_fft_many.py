from numpy import *
import cmath as cmath
from matplotlib import pyplot as plt
from scipy.integrate import odeint
from datetime import datetime

def func(y, t, N_osc, omg, gamma):
    y_help = zeros((N_osc))
    for i in arange(N_osc):
        y_help[i] = sum(sin(y-y[i]))
    return (omg + gamma*y_help/N_osc)
    
#def grad(y, t, N_osc):    return [[0,t], [1,0]]

# system parameter
N_osc  = 1000           # number of osci
spread = 1         # spread of osci distrib.
omg    = sort(spread*random.randn(N_osc))
gamma  = 1.85          # coupling strength
#plt.figure(0)
#plt.hist(omg)

# intergration parameter   
N_time = 10000
tmax   = 1000.
y0     = (4*random.randn(N_osc))%(2.*pi)                # initial condition
t      = linspace(0, tmax, N_time)      # time points startin with init cond
y      = odeint(func, y0, t, (N_osc, omg, gamma))%(2*pi)#, Dfun=grad)
file   = open("../pics_zu_github/integrator.txt",'w')
file.write("integration with\n N_osc ="+repr(N_osc)+"\n")
file.write("omg = randn, spread = "+repr(spread)+"\n")
file.write("gamma = "+repr(gamma)+"\n")
file.write("N_time = "+repr(N_time)+"\n")
file.write("tmax = "+repr(tmax)+"\n")
file.write(str(y))

order  = ones(N_time)+1j*ones(N_time)
phi    = ones(N_time)
phi_corr = ones(N_time)
phase2pi = 0
for i in arange(N_time):
    order[i] = sum(cos(y[i])+1j*sin(y[i]))/N_osc
    phi[i] = cmath.phase(order[i])
    if (phi[i]-phi[i-1])>(pi):
        phase2pi = phase2pi - 2.*pi   
    if (-phi[i]+phi[i-1])>(pi):
        phase2pi = phase2pi + 2.*pi
    phi_corr[i] = phi[i] + phase2pi

lin = phi_corr[100-1:]
omg_mean = 0 
for k in arange(len(lin)-1)+1:
    omg_mean = omg_mean + lin[k]/k

phi_corr_fluct = lin + sum(lin)/len(lin)
fft = fft.fft(phi_corr_fluct)
#freqban = 
    
       
    
#print(order)
plt.figure(1)
#plt.plot(y)
plt.plot(order.real,order.imag)
plt.plot(order.real[0:20],order.imag[0:20])
plt.plot(order.real[N_time-20:N_time-1],order.imag[N_time-20:N_time-1])
plt.figure(2)
plt.plot(abs(order))
plt.figure(3)
#plt.plot(phi)
plt.plot(phi_corr_fluct)
plt.plot(phi_corr)
plt.figure(4)
plt.plot(fft)
plt.figure(5)
plt.plot(omg)
file.close()
plt.show()

#><
