from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np

def sir(y,t):
        S = y[0]
        I = y[1]
        R = y[2]
        N = S + I + R
        beta = 1/2 # how often a susceptible-infected contact results in a new infection
        gamma = 1/3 # rate at which an infected recovers and becomes resistant
        return np.array([ -beta*(S*I/N), beta*(S*I/N)-gamma*I, gamma*I ])

time = np.linspace(0.0, 10.0, 1000)
yinit = np.array([10,1,0])
y = odeint(sir, yinit, time)

print(y)

plt.plot(time, y[:,0], 'g', label="Susceptible")
plt.plot(time, y[:,1], 'r', label="Infected")
plt.plot(time, y[:,2], 'b', label="Recovered")

plt.title("SIR Model")

plt.xlabel('t')
plt.ylabel('y')

plt.legend()

plt.savefig('test.png')
