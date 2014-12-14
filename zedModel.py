from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np

def hzd(y,t):
        H = y[0]
        Z = y[1]
        D = y[2]
        alpha = 4.8 # rate at which humans become zombies
                    # (i.e. probability of being infected when you come in contact with the infected)
        beta = .05  # rate at which zombies die
                    # (i.e. probability of dying when you come in contact with a human)
        gamma = .2 # rate at which humans die (without becoming zombies)
                    # (i.e. probability of dying when you come in contact with another human)
        return np.array([ -alpha*Z - gamma*H, alpha*Z - beta*H, beta*H + gamma*H ])

nsteps = 3000
ndays = 30
stepsPerDay = nsteps/ndays

time = np.linspace(0.0, ndays, num=nsteps)
yinit = np.array([0.99,0.01,0])
y = odeint(hzd, yinit, time)

finaly = []
for row in y:
    if row[0] <= 0 or row[1] <= 0:
        # no humans or zombies left, crisis resolved
        break
    else:
        finaly.append(row)

finaly = np.array(finaly)
finalSteps = len(finaly[:,0])
finalDays = finalSteps/stepsPerDay
sums = np.reshape(np.sum(finaly, axis=1), (finalSteps,1))
finaly = np.concatenate((finaly, sums), axis=1)
finaltime = np.linspace(0.0, finalDays, finalSteps)

plt.plot(finaltime, finaly[:,0], color='green', label="Humans")
plt.plot(finaltime, finaly[:,1], color='red', label="Zombies")
plt.plot(finaltime, finaly[:,2], color='black', label="Inanimate Dead")

plt.title("HZD Zombie Outbreak Model")

plt.xlabel('Days since Z-Day')
plt.ylabel('Percentage of Population')

plt.legend(loc="best")

plt.show()
plt.savefig('test.png')
