from tiles import tile
import numpy as np
from random import randint

class Grid:
    def __init__(self, w, h):
        # create the map
        self.h = h
        self.w = w
        self.grid = [[0 for x in range(w)] for y in range(h)]
        # fill it with tile objects
        for y in range(h):
            for x in range(w):
                pop = [randint(1,100),randint(0,5),0]
                loc = [x,y]
                self.grid[x][y] = tile(pop,loc)

    def debugDisplay(self):
        for row in self.grid:
            print(row)

