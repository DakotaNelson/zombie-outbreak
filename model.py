from tiles import tile, bordertile
import numpy as np
from random import randint
import math

class Grid:
    def __init__(self, size):
        # create the map
        self.h = size
        self.w = size
        self.grid = [[0 for x in range(self.w)] for y in range(self.h)]
        # populate the edges
        for x in range (self.w):
            loc = [x, 0]
            self.grid[x][0] = bordertile(loc)
            loc = [x, self.h-1]
            self.grid[x][self.h-1] = bordertile(loc)
        for y in range (self.h):
            loc = [0, y]
            self.grid[0][y] = bordertile(loc)
            loc = [self.w-1, y]
            self.grid[self.w-1][y] = bordertile(loc)
        # fill it with tile objects
        cen = [randint(1,50),randint(1,50)]
        for y in range(1, self.h-1):
            for x in range(1, self.w-1):
                if randint(1,10000) <= 30:
                    # how likely there is to be a zombie on any given square
                    zombies = randint(1,3)
                else:
                    zombies = 0
                pop = [randint(1,100),zombies,0]
                loc = [x,y]
                self.grid[x][y] = tile(pop,loc,cen)
        for m in range(2):
            for y in range(1, self.h-1):
                for x in range(1, self.w-1):
                    self.grid[x][y].findneighbors(self.grid)

    def debugDisplay(self):
        for row in self.grid:
            print(row)

    def printSquare(self, pos):
        print self.humans(pos)
        print self.zombies(pos)
        print self.dead(pos)

    def zombies(self, pos):
        ''' get number of zombies at a position '''
        return self.grid[pos[0]][pos[1]].zom

    def humans(self, pos):
        ''' get number of humans at a position '''
        return self.grid[pos[0]][pos[1]].hum

    def dead(self, pos):
        ''' get number of bodies at a position '''
        return self.grid[pos[0]][pos[1]].ded

    def totalZombies(self):
        ''' get number of zombies on the map '''
        return self.total('zom')

    def totalHumans(self):
        ''' get number of humans on the map '''
        return self.total('hum')

    def totalDead(self):
        ''' get number of bodies on the map '''
        return self.total('ded')

    def total(self, thing):
        ''' get number of [thing] on the map '''
        total = 0
        for y in range(self.h):
            for x in range(self.w):
                tile = self.grid[x][y]
                total += getattr(tile,thing)
        return total

    def destroy(self, humans, zombies, pos):
        ''' destroy some humans and zombies at a position '''
        self.grid[pos[0]][pos[1]].hum -= int(humans)
        self.grid[pos[0]][pos[1]].zom -= int(zombies)

        if self.grid[pos[0]][pos[1]].hum < 0: self.grid[pos[0]][pos[1]].hum = 0
        if self.grid[pos[0]][pos[1]].zom < 0: self.grid[pos[0]][pos[1]].zom = 0

        self.grid[pos[0]][pos[1]].ded += int(humans + zombies)
        return [self.grid[pos[0]][pos[1]].hum,
                self.grid[pos[0]][pos[1]].zom,
                self.grid[pos[0]][pos[1]].ded]

    def neighborDestroy(self, humans, zombies, pos):
        ''' destroy some humans and zombies in a position's immediate neighbors '''
        x = pos[0]
        y = pos[1]
        if x>0:
            self.destroy(humans, zombies, [x-1,y])
        if x<self.w-1:
            self.destroy(humans, zombies, [x+1,y])
        if y>0:
            self.destroy(humans, zombies, [x,y-1])
        if y<self.h-1:
            self.destroy(humans, zombies, [x,y+1])

    def add(self, humans, zombies, pos):
        '''add some humans and zombies at a position'''
        self.grid[pos[0]][pos[1]].hum += int(humans)
        self.grid[pos[0]][pos[1]].zom += int(zombies)

        return [self.grid[pos[0]][pos[1]].hum,
                self.grid[pos[0]][pos[1]].zom,
                self.grid[pos[0]][pos[1]].ded]

    def destroyPercent(self, humPercent, zomPercent, pos):
        ''' destroy a percentage of humans and zombies at a position '''
        humCasualties = math.ceil(humPercent * self.humans(pos))
        zomCasualties = math.ceil(zomPercent * self.zombies(pos))

        return self.destroy(humCasualties, zomCasualties, pos)

    def neighborDestroyPercent(self, humanPercent, zombiePercent, pos):
        ''' destroy a percentage of humans and zombies in a position's immediate neighbors '''
        x = pos[0]
        y = pos[1]
        if x>0:
            self.destroyPercent(humanPercent, zombiePercent, [x-1,y])
        if x<self.w-1:
            self.destroyPercent(humanPercent, zombiePercent, [x+1,y])
        if y>0:
            self.destroyPercent(humanPercent, zombiePercent, [x,y-1])
        if y<self.h-1:
            self.destroyPercent(humanPercent, zombiePercent, [x,y+1])


    def update(self):
        ''' advance the DEs by one tick '''
        for y in range(1, self.h-1):
            for x in range(1, self.w-1):
                self.grid[x][y].popout()
                self.grid[x][y].update()
        return


class Resources:
    def __init__(self, difficulty):
        # difficulty should be 1-5
        if difficulty < 1: difficulty = 1
        if difficulty > 5: difficulty = 5
        booty = 6 - int(difficulty)
        # input (difficulty): 1 = easiest, 5 = hardest
        # output (booty): 5 = most resources, 1 = least

        # with great booty comes great numbers of armaments
        self.airstrikes = randint(1,10) * booty
        self.infantry = randint(5,20) * 50 * booty

class Metadata:
    def __init__(self, data):
        self.days = 0 # number of days in the game that have passed
        self.initialHumans = data.totalHumans()

    def update(self):
        # run each tick
        self.days += 1
