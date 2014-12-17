import random

class tile(object):
    def __init__(self, pop, loc):
        self.x = loc[0]
        self.y = loc[1]
        self.iswater()
        if self.iswater:
            pop = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.hum = pop[0]
        self.inf = pop[1]
        self.zom = pop[2]
        self.ded = pop[3]
        self.gon = pop[4]

    def iswater(self):
        waterprob = abs(self.x - 50.0) * abs(self.y - 50.0)
        ran = random.randint(0, 2500)
        if ran > waterprob:
            self.iswater = False
        if ran < waterprob:
            self.iswater = True

    def popadd(self, pop):
        if not self.iswater:
            self.hum += pop[0]
            self.inf += pop[1]
            self.zom += pop[2]
            self.ded += pop[3]
            self.gon += pop[4]

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
    initpop = [10, 1, 3, 1, 1]
    loc = [20, 4]
    home = tile(initpop, loc)
    print home.hzrat()
    home.popadd([1,1,2,1,1])
    print home.hzrat()
    print home.color()

if __name__ == "__main__":
    main()



