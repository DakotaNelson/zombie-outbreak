import random
import numpy as np

class tile(object):
    def __init__(self, pop, loc):
        self.x = loc[0]
        self.y = loc[1]
        self.iswater()
        if self.iswater:
            pop = [0.0, 0.0, 0.0]
        self.hum = pop[0]
        self.zom = pop[1]
        self.ded = pop[2]

    def iswater(self):
        waterprob = abs(self.x - 50.0) * abs(self.y - 50.0)
        ran = random.randint(0, 2500)
        if ran > waterprob:
            self.iswater = False
        if ran < waterprob:
            self.iswater = True

    def findneighbors(self,tilegrid):
        self.left = tilegrid[x-1, y]
        self.up = tilegrid[x, y-1]
        self.down = tilegrid[x, y+1]
        self.right = tilegrid[x+1, y]

    def popadd(self, pop):
        if not self.iswater:
            self.hum += pop[0]
            self.zom += pop[1]
            self.ded += pop[2]

    def popout(self)
        lefthz = self.left.hzrat()
        uphz = self.up.hzrat()
        downhz = self.down.hzrat()
        righthz = self.right.hzrat()
        #placeholder math
        leftpop = .1*self.hzrat()*lefthz
        uppop = .1*self.hzrat()*uphz
        downpop = .1*self.hzrat()*downhz
        rightpop = .1*self.hzrat()*righthz
        self.left.popadd(leftpop)
        self.up.popadd(uppop)
        self.down.popadd(downpop)
        self.right.popadd(rightpop)

    def hzrat(self):
        try:
            return float(self.hum)/float(self.zom)
        except ZeroDivisionError:
            return float(self.hum)

    def color(self):
        if self.iswater:
            return [0, 0, 255]
        else:
            red = int(51*(1.0/self.hzrat()))
            if red > 255: red = 255
            green = int(51*self.hzrat())
            if green > 255: green = 255
            return [red, green, 0]

def main():
    initpop = [10, 3, 1]
    loc = [20, 4]
    home = tile(initpop, loc)
    print home.hzrat()
    home.popadd([1,2,1])
    print home.hzrat()
    print home.color()
    x = np.array([[1,2],[3,4]])
    print x[1,1]

if __name__ == "__main__":
    main()



