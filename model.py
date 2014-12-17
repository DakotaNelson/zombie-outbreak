from tiles import tile
import numpy as np
from random import randint

class Grid:
    def __init__(self, size):
        # create the map
        self.h = size
        self.w = size
        self.grid = [[0 for x in range(self.w)] for y in range(self.h)]
        # fill it with tile objects
        for y in range(self.h):
            for x in range(self.w):
                if randint(1,10000) <= 10:
                    zombies = randint(1,3)
                else:
                    zombies = 0
                pop = [randint(1,100),zombies,0]
                loc = [x,y]
                self.grid[x][y] = tile(pop,loc)
                #TODO edge cases should be border tile
                #TODO filter out small specks of land

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

    def destroy(self, humans, zombies, pos):
        ''' destroy some humans and zombies at a position '''
        self.grid[pos[0]][pos[1]].hum -= int(humans)
        self.grid[pos[0]][pos[1]].zom -= int(zombies)

        if self.grid[pos[0]][pos[1]].hum < 0: self.grid[pos[0]][pos[1]].hum = 0
        if self.grid[pos[0]][pos[1]].zom < 0: self.grid[pos[0]][pos[1]].zom = 0

        self.grid[pos[0]][pos[1]].ded += int(humans + zombies)
        return [self.grid[pos[0]][pos[1]].hum, self.grid[pos[0]][pos[1]].zom, self.grid[pos[0]][pos[1]].ded]

    def update(self):
        ''' advance the DEs by one tick '''
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
