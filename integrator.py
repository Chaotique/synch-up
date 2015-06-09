"""
this program is work before progress/play ground (finite size Kuramoto modell, franziska peter), go to follow-ups to get some doku,

apropos doku, zu diesem programm gehoert ein dokumentationsmodul, das bilder und die parameter in ein tex-file exportiert.
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
    y_help = zeros((N_osc))
    for i in arange(N_osc):
        y_help[i] = sum(sin(y-y[i]))
    return (omg + epsilon*y_help/N_osc)
    
# system parameter
N_osc  = 25             # number of osci
spread = 1              # spread of osci distrib.
omg    = sort(spread*random.randn(N_osc))
epsilon  = 1.5          # coupling strength


# intergration parameter   
N_time = 7000
tmax   = 300.
y0     = (4*random.randn(N_osc))%(2.*pi)                # initial condition
t      = linspace(0, tmax, N_time)      # time points startin with init cond
y      = odeint(func, y0, t, (N_osc, omg, epsilon))%(2*pi)#, Dfun=grad)

# documentation
myfile = open(os.path.basename(__file__) + ".tex", "a+b")
filename1 = dokufile(myfile)

# order parameter, phase
order  = ones(N_time)+1j*ones(N_time)
phi    = ones(N_time)
for i in arange(N_time):
    order[i] = sum(cos(y[i])+1j*sin(y[i]))/N_osc
    phi[i] = cm.phase(order[i])
    
# plotting / saving pics
scale = 0.3
plt.figure(1)
ax= plt.subplot(111, polar=True)
ax.plot(phi,abs(order))
ax.plot(phi[0:20],abs(order[0:20]), label = 'start')
ax.plot(phi[N_time-20:N_time-1],abs(order[N_time-20:N_time-1]), label = 'end')
ax.set_rmax(1.1)
plt.legend(loc = 'best')
ax.grid(True)
savepictopdfandtex('integratororder', filename1, plt, myfile, scale)

plt.figure(2)
plt.plot(abs(order), label = 'mf order parameter')
plt.plot(phi, label = 'mf phase')
plt.legend(loc = 'best')
xl = plt.xlabel('t')
plt.title('mean field Kuramoto, N_osc ='+repr(N_osc)+"\n")
plt.grid(True)
savepictopdfandtex('integratorImRe', filename1, plt, myfile, scale)

plt.show()

# closing documentation with comment
enddoku(N_osc, spread, epsilon, N_time, tmax, myfile)
