import random
import numpy as np
from scipy.integrate import odeint

class bordertile(object):
    '''dummy class for border tiles. gets rid of edge cases.'''
    def __init__(self, loc):
        self.x = loc[0]
        self.y = loc[1]
        #border tiles are always water
        self.iswater = True

    def hzrat():
        #return is the same as it is for all water tiles
        return 0.0

class tile(object):
    '''class for tiles on the map. each tile has a population. sometimes it is water'''
    def __init__(self, pop, loc):
        '''initializes each tile with a location, a population, and a water state'''
        self.x = loc[0]
        self.y = loc[1]
        self.iswaterinit()
        #no population if the tile is full of water
        if self.iswater:
            pop = np.array([0.0, 0.0, 0.0])
        self.hum = pop[0]
        self.zom = pop[1]
        self.ded = pop[2]

    def hzd(self):
        alpha = 4.8 # rate at which humans become zombies
        # (i.e. probability of being infected when you come in contact with the infected)
        beta = .05  # rate at which zombies die
        # (i.e. probability of dying when you come in contact with a human)
        gamma = .2 # rate at which humans die (without becoming zombies)
        # (i.e. probability of dying when you come in contact with another human)
        return np.array([
                -alpha*self.zom - gamma*self.hum,
                alpha*self.zom - beta*self.hum,
                beta*self.hum + gamma*self.hum])

    def update(time):
        '''given an array of time values, spits out a new population'''
        pop = np.array([self.hum, self.zom, self.ded])
        poplist = odeint(hzd, pop, time)
        newpop = pop[-1]
        self.hum = pop[0]
        self.zom = pop[1]
        self.ded = pop[2]

    def iswaterinit(self):
        '''on startup, determine whether or not this tile is water'''
        waterprob = abs(self.x - 50.0) * abs(self.y - 50.0)
        ran = random.randint(0, 2500)
        if ran >= waterprob:
            self.iswater = False
        if ran < waterprob:
            self.iswater = True

    def findneighbors(self,tilegrid):
        '''once the entire grid is populated with tiles, find the neighbors'''
        self.left = tilegrid[self.y, self.x-1]
        self.up = tilegrid[self.y-1, self.x]
        self.down = tilegrid[self.y+1, self.x]
        self.right = tilegrid[self.y, self.x+1]

    def popadd(self, pop):
        '''add population from people moving when neighbors run popout()'''
        if not self.iswater:
            self.hum += pop[0]
            self.zom += pop[1]
            self.ded += pop[2]
        else:
            pass

    def popout(self):
        '''simulates population emigration'''
        #get ratios
        lefthzf = self.left.hzrat()
        uphzf = self.up.hzrat()
        downhzf = self.down.hzrat()
        righthzf = self.right.hzrat()
        neighbhz = lefthzf + uphzf + downhzf + righthzf
        #calculate outflow
        outflow = (0.6/(self.hzrat+1))
        zout = outflow*self.zom
        hout = outflow*self.hum
        #comment on american consumerism
        leftpop = [hout*lefthzf/neighbhzf, zout*lefthzf/neighbhzf, 0]
        uppop = [hout*lefthzf/neighbhzf, zout*uphzf/neighbhzf, 0]
        downpop = [hout*lefthzf/neighbhzf, zout*downhzf/neighbhzf, 0]
        rightpop = [hout*lefthzf/neighbhzf, zout*righthzf/neighbhzf, 0]
        #now increment everything
        self.left.popadd(leftpop)
        self.up.popadd(uppop)
        self.down.popadd(downpop)
        self.right.popadd(rightpop)

    def hzrat(self):
        '''calculate the human-zombie ratio. used for math later'''
        try:
            return float(self.hum)/float(self.zom)
        except ZeroDivisionError:
            return float(self.hum)

    def color(self):
        '''generate a color for the tile. to be used in pygame'''
        if self.iswater:
            return [0, 0, 255]
        else:
            try:
                red = int(51*(1.0/self.hzrat()))
                if red > 255: red = 255
            except ZeroDivisionError:
                red = 255
            green = int(51*self.hzrat())
            if green > 255: green = 255
            return [red, green, 0]

def main():
    '''main function. runs on file call.'''
    initpop = [10, 3, 1]
    loc = [1, 1]
    home = tile(initpop, loc)
    left = tile(initpop, [0, 1])
    right = tile(initpop, [2, 1])
    down = tile(initpop, [1, 2])
    up = tile(initpop, [1, 0])
    tilegrid = np.array([[0, up, 0],[left,home,right],[0,down,0]])
    home.findneighbors(tilegrid)
    print home.hzrat()
    home.popadd([1,2,1])
    print home.hzrat()
    print home.color()
    x = np.array([[1,2],[3,4]])
    print x[1]

if __name__ == "__main__":
    main()



