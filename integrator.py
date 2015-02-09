from numpy import *
from matplotlib import pyplot as plt
from scipy.integrate import odeint

def func(y, t, N_osc, omg, gamma, order):
    y_help = zeros((N_osc))
    for i in arange(N_osc):
        y_help[i] = sum(sin(y-y[i]))
    return (omg + gamma*y_help/N_osc)
    
#def grad(y, t, N_osc):    return [[0,t], [1,0]]

# system parameter
N_osc  = 100           # number of osci
spread = 1         # spread of osci distrib.
omg    = sort(spread*random.randn(N_osc))
gamma  = 0.7           # coupling strength
#plt.figure(0)
#plt.hist(omg)

# intergration parameter   
N_time = 5000
tmax   = 10.
y0     = (4*random.randn(N_osc))%(2.*pi)                # initial condition
t      = linspace(0, tmax, N_time)      # time points startin with init cond
y      = odeint(func, y0, t, (N_osc, omg, gamma))%(2*pi)#, Dfun=grad)
file   = open("integrator.txt",'w')
file.write("integration with\n N_osc ="+repr(N_osc)+"\n")
file.write("omg = randn, spread = "+repr(spread)+"\n")
file.write("gamma = "+repr(gamma)+"\n")
file.write("N_time = "+repr(N_time)+"\n")
file.write("tmax = "+repr(tmax)+"\n")
file.write(str(y))

order  = ones(N_time)+1j*ones(N_time)
for i in arange(N_time):
    order[i] = sum(cos(y[i])+1j*sin(y[i]))/N_osc

#print(order)
plt.figure(1)
#plt.plot(y)
plt.plot(order.real,order.imag)
plt.plot(order.real[0:20],order.imag[0:20])
plt.plot(order.real[N_time-20:N_time-1],order.imag[N_time-20:N_time-1])
plt.figure(2)
plt.plot(abs(order))
file.close()
plt.show()
