"""

"""


from numpy import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cmath as cmath
from scipy.integrate import odeint
import pylab as P
from datetime import datetime

def func(y, t, N_osc, omg, gamma):
    y_help = zeros((N_osc))
    for i in arange(N_osc):
        y_help[i] = sum(sin(y-y[i]))
    return (omg + gamma*y_help/N_osc)
    
#def grad(y, t, N_osc):    return [[0,t], [1,0]]

# system parameter
N_osc  = 100           # number of osci
spread = 1.            # spread of osci distrib.
omg    = sort(spread*random.randn(N_osc))
print(omg)
gamma  = 1.85          # coupling strength

# intergration parameter   
N_time = 20000
tmax   = 2000
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


# variance and mean of the phase as a function of time
mean_phi = zeros(len(lin))
variance_phi = zeros(len(lin))
for i in arange(len(lin)-50)+50:
    mean_phi[i] = mean(lin[(i-50):(i+50)])
    
X_mu = lin-mean_phi
for i in arange(len(X_mu)-50)+50:
    variance_phi[i] = mean(X_mu[(i-50):(i+50)]**2)
    
       
    
#print(order)
plt.figure(1)
#plt.plot(y)
plt.plot(order.real,order.imag)
plt.plot(order.real[0:20],order.imag[0:20])
plt.plot(order.real[N_time-20:N_time-1],order.imag[N_time-20:N_time-1])
plt.figure(2)
plt.plot(abs(order))
plt.figure(3)
plt.plot(phi)
plt.plot(phi_corr)
plt.plot(phi_corr_fluct)
plt.figure(7)
#plt.plot((lin-mean_phi)[50:])
plt.plot(variance_phi[100:-100])
plt.figure(4)
plt.plot(fft)
plt.figure(5)
plt.plot(omg)
file.close()
fig = plt.figure(6)
x = linspace(-1.,1.,200)
yo = sqrt(1-x**2)
yu = -sqrt(1-x**2)
plt.plot(x,yo,'b')
plt.plot(x,yu,'b')
ims = []
for i in range(N_time):
    x1 = sin(y[i])
    x2 = cos(y[i])
    im, = plt.plot(x1,x2, 'bo')
    ims.append([im])

ani = animation.ArtistAnimation(fig, ims, interval=100, blit=True, repeat_delay=1000)

ani.save('../pics_zu_github/dynamicimages.mp4')

plt.figure(7)
bins = linspace(0,1,100)
# the histogram of the data with histtype='step'
n, bins, patches = P.hist(abs(order[100:N_time]), bins, normed=1, histtype='bar', rwidth=0.8)

plt.show()
