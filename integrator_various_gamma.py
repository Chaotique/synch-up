from numpy import *
import cmath as cm
from matplotlib import pyplot as plt
from scipy.integrate import odeint
from datetime import datetime

def func(y, t, N_osc, omg, gamma):
    y_help = zeros((N_osc))
    for i in arange(N_osc):
        y_help[i] = sum(sin(y-y[i]))
    return (omg + gamma*y_help/N_osc)
    

# system parameter
N_osc  = 500           # number of osci
spread = 1         # spread of osci distrib.
omg    = sort(spread*random.randn(N_osc))
gamma  = 5          # coupling strength
#plt.figure(0)
#plt.hist(omg)

# intergration parameter   
N_time = 1000
tmax   = 100.
y0     = (4*random.randn(N_osc))%(2.*pi)                # initial condition
t      = linspace(0, tmax, N_time)      # time points startin with init cond
g = linspace(0.7,6,10)

"""
f, ((ax1, ax2, ax3, ax4, ax5), (ax6, ax7, ax8, ax9, ax10)) = plt.subplots(2, 5, sharex='col', sharey='row')
x = linspace(0,10,100)
y = linspace(0,10,100)
ax1.plot(x, y)
ax1.set_title('Sharing x per column, y per row')
ax2.scatter(x, y)
ax3.scatter(x, 2 * y ** 2 - 1, color='r')
ax4.plot(x, 2 * y ** 2 - 1, color='r')
ax5.plot(x, 2 * y ** 2 - 1, color='r')
ax6.plot(x, 2 * y ** 2 - 1, color='r')
ax7.plot(x, 2 * y ** 2 - 1, color='r')
ax8.plot(x, 2 * y ** 2 - 1, color='r')
"""

for i in arange(10):
    gamma  = g[i]
    y      = odeint(func, y0, t, (N_osc, omg, gamma))%(2*pi)#, Dfun=grad)
    #file   = open("integrator.txt",'w')
    #file.write("integration with\n N_osc ="+repr(N_osc)+"\n")
    #file.write("omg = randn, spread = "+repr(spread)+"\n")
    #file.write("gamma = "+repr(gamma)+"\n")
    #file.write("N_time = "+repr(N_time)+"\n")
    #file.write("tmax = "+repr(tmax)+"\n")
    #file.write(str(y))

    order  = ones(N_time)+1j*ones(N_time)
    phi    = ones(N_time)
    for i in arange(N_time):
        order[i] = sum(cos(y[i])+1j*sin(y[i]))/N_osc
        phi[i] = cm.phase(order[i])
    

    #print(order)
    plt.figure(1)
    #plt.plot(y)
    plt.plot(order.real,order.imag)
    #plt.plot(order.real[0:20],order.imag[0:20])
    #plt.plot(order.real[N_time-20:N_time-1],order.imag[N_time-20:N_time-1])
    plt.figure(2)
    plt.plot(abs(order))
    plt.figure(3)
    plt.plot(phi)

#file.close()
plt.show()
