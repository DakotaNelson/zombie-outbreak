import random

import math
import numpy as np
from scipy.integrate import odeint

class bordertile(object):
    '''dummy class for border tiles. gets rid of edge cases.'''
    def __init__(self, loc):
        self.x = loc[0]
        self.y = loc[1]
        #border tiles are always water
        self.iswater = True
        self.hum = 0
        self.zom = 0
        self.ded = 0

    def color(self):
        return [0, 0, 255]

    def popadd(self,pop):
        self.hum = 0
        self.zom = 0
        self.ded = 0

    def hzrat(self):
        #return is the same as it is for all water tiles
        return 0.0

    def hzdef(self):
        return 0.0

class tile(object):
    '''class for tiles on the map. each tile has a population. sometimes it is water'''
    def __init__(self, pop, loc, cen):
        '''initializes each tile with a location, a population, and a water state'''
        self.x = loc[0]
        self.y = loc[1]
        self.iswaterinit(cen)
        #no population if the tile is full of water
        if self.iswater:
            pop = [0, 0, 0]
        self.hum = pop[0]
        self.zom = pop[1]
        self.ded = pop[2]

    def hzd(self):
        if self.iswater:
            return [0, 0, 0]
        alpha = 1.3 # rate at which humans become zombies
        # (i.e. probability of being infected when you come in contact with the infected)
        beta = 1  # rate at which zombies die
        # (i.e. probability of dying when you come in contact with a human)
        gamma = .00002 # rate at which humans die (without becoming zombies)
        # (i.e. probability of dying when you come in contact with another human)
        N = self.oldZom + self.oldHum + self.oldDed
        h2z = (alpha * self.oldZom * self.oldHum) // N  # humans -> zombies
        z2d = (beta * self.oldHum * self.oldZom) // N # zombies -> dead
        h2d = (gamma * self.oldHum * self.oldHum) // N # humans -> dead

        #if self.x == 20 and self.y == 20:
            #print N

        if random.random() < alpha: h2z = math.ceil(h2z)
        else: h2z = math.floor(h2z)

        if random.random() < beta: z2d = math.ceil(z2d)
        else: z2d = math.floor(z2d)

        if random.random() < gamma: h2d = math.ceil(h2d)
        else: h2d = math.floor(h2d)

        # don't create more zombies than there are humans
        if h2z+h2d > self.hum: h2z = self.hum - h2d # give priority to humans killing each other

        if z2d > self.zom: z2d = -self.zom

        deltaH = -h2z-h2d
        deltaZ = h2z-z2d

        # never kill more humans or zombies than exist
        if self.oldHum+deltaH < 0: deltaH = -self.oldHum
        if self.oldZom+deltaZ < 0: deltaZ = -self.oldZom

        return [deltaH, deltaZ, z2d+h2d]

    def update(self):
        '''spits out a new population one time step in the future'''

        self.oldHum = self.hum
        self.oldZom = self.zom
        self.oldDed = self.ded

        # then apply the hzd model
        step = self.hzd()
        self.hum += int(step[0])
        self.zom += int(step[1])
        self.ded += int(step[2])

    def iswaterinit(self, cen):
        '''on startup, determine whether or not this tile is water'''
        waterprob = abs(self.x - float(cen[0])) * abs(self.y - float(cen[1]))
        ran = random.randint(0, cen[0]*cen[1])
        if ran >= .3*waterprob:
            self.iswater = False
        if ran < .3*waterprob:
            self.iswater = True

    def findneighbors(self,tilegrid):
        '''once the entire grid is populated with tiles, find the neighbors'''
        self.left = tilegrid[self.x-1][self.y]
        self.up = tilegrid[self.x][self.y-1]
        self.down = tilegrid[self.x][self.y+1]
        self.right = tilegrid[self.x+1][self.y]
        horiz = [self.left.iswater, self.right.iswater]
        vert = [self.up.iswater, self.down.iswater]
        #lowpass filter
        if horiz == [True, True] or vert == [True, True]:
            if self.iswater == False:
                self.iswater = True
        if horiz == [False, False] or vert == [False, False]:
            if self.iswater == True:
                self.iswater == False

        self.oldHzrat = self.hzrat()
        self.oldLeftHzrat = self.left.hzrat()
        self.oldUpHzrat = self.up.hzrat()
        self.oldRightHzrat = self.right.hzrat()
        self.oldDownHzrat = self.down.hzrat()
        self.oldZom = self.zom
        self.oldHum = self.hum

    def popadd(self, pop):
        '''add population from people moving when neighbors run popout()'''
        if not self.iswater:
            self.hum += pop[0]
            self.zom += pop[1]
            self.ded += pop[2]
        else:
            pass

    def hzdef(self):
        '''calculate the human-zombie difference. used for math later'''
        return self.hum - self.zom

    def popout(self):
        '''simulates population emigration'''
        #get ratios
        lefthzf = self.oldLeftHzrat
        uphzf = self.oldUpHzrat
        downhzf = self.oldDownHzrat
        righthzf = self.oldRightHzrat
        neighbhzf = lefthzf + uphzf + downhzf + righthzf
        if neighbhzf == 0:
            neighbhzf = 1
        #calculate outflow
        outflow = (0.5/(self.oldHzrat+1))
        zout = math.ceil(outflow*self.oldZom)
        hout = math.ceil(outflow*self.oldHum)
        #comment on american consumerism
        leftpop = [hout*lefthzf//neighbhzf, zout*lefthzf//neighbhzf, 0]
        uppop = [hout*uphzf//neighbhzf, zout*uphzf//neighbhzf, 0]
        downpop = [hout*downhzf//neighbhzf, zout*downhzf//neighbhzf, 0]
        rightpop = [hout*righthzf//neighbhzf, zout*righthzf//neighbhzf, 0]
        outpop = [0, 0, 0]
        for i in range(3):
            outpop[i] = -1*(leftpop[i] + uppop[i] + downpop[i] + rightpop[i])
        # store current variables for next time
        self.oldHzrat = self.hzrat()
        self.oldLeftHzrat = self.left.hzrat()
        self.oldUpHzrat = self.up.hzrat()
        self.oldRightHzrat = self.right.hzrat()
        self.oldDownHzrat = self.down.hzrat()
        self.oldZom = self.zom
        self.oldHum = self.hum
        #now increment everything
        self.left.popadd(leftpop)
        self.up.popadd(uppop)
        self.down.popadd(downpop)
        self.right.popadd(rightpop)
        self.popadd(outpop)

    def popout2(self):
        '''simulates population emigration'''
        #calculate local ratios
        selfhzf = self.oldHzrat
        lefthzf = self.oldLeftHzrat
        uphzf = self.oldUpHzrat
        downhzf = self.oldDownHzrat
        righthzf = self.oldRightHzrat
        lefthzr = lefthzf - selfhzf
        uphzr = uphzf - selfhzf
        downhzr = downhzf - selfhzf
        righthzr = righthzf - selfhzf
        hzrlist = [lefthzr, uphzr, downhzr, righthzr]
        hzrsum = 0
        for i in xrange(len(hzrlist)):
            if hzrlist[i] < 0:
                hzrlist[i] = 0
            hzrsum += hzrlist[i]
        if hzrsum < .01: hzrsum = 1
        #comment on american consumerism
        leftpop = [.4*hzrlist[0]/hzrsum*self.oldHum, .4*hzrlist[0]/hzrsum*self.oldZom, 0]
        uppop = [.4*hzrlist[1]/hzrsum*self.oldHum, .4*hzrlist[1]/hzrsum*self.oldZom, 0]
        downpop = [.4*hzrlist[2]/hzrsum*self.oldHum, .4*hzrlist[2]/hzrsum*self.oldZom, 0]
        rightpop = [.4*hzrlist[3]/hzrsum*self.oldHum, .4*hzrlist[3]/hzrsum*self.oldZom, 0]
        if self.left.iswater: leftpop = [0, 0, 0]
        if self.up.iswater: uppop = [0, 0, 0]
        if self.down.iswater: downpop = [0, 0, 0]
        if self.right.iswater: rightpop = [0, 0, 0]
        outpop = [0, 0, 0]
        for i in range(3):
            outpop[i] = -1*(leftpop[i] + uppop[i] + downpop[i] + rightpop[i])
        # store current variables for next time
        self.oldHzrat = self.hzrat()
        self.oldLeftHzrat = self.left.hzrat()
        self.oldUpHzrat = self.up.hzrat()
        self.oldRightHzrat = self.right.hzrat()
        self.oldDownHzrat = self.down.hzrat()
        self.oldZom = self.zom
        self.oldHum = self.hum
        #now increment everything
        self.left.popadd(leftpop)
        self.up.popadd(uppop)
        self.down.popadd(downpop)
        self.right.popadd(rightpop)
        self.popadd(outpop)

    def hzrat(self):
        '''calculate the human-zombie ratio. used for math later'''
        if False:
           pass
        #if self.hum == 0 and self.zom == 0:
        #    return 0.1
        else:
            try:
                return (float(self.hum + 1))/(float(self.zom)+float(self.hum))
            except ZeroDivisionError:
                return 0.0

    def color(self):
        '''generate a color for the tile. to be used in pygame'''
        if self.iswater:
            return [0, 0, 255]
        else:
            red = int(5*self.zom)
            if red < 0: red = 0
            if red > 255: red = 255
            green = int(255*self.hzrat())
            if green < 0: green = 0
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



