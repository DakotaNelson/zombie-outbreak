from math import ceil
from random import randint

class Controller:
    def __init__(self, grid):
        self.grid = grid
        return

    def airstrike(self, pos):
        # launch an airstrike on a tile
        print "airstrike at: " + str(pos)

        print "before"
        self.grid.printSquare(pos)

        humPercent = float(randint(0, 30)) / 100.0
        zomPercent = float(randint(40, 80)) / 100.0

        humCasualties = ceil(humPercent * self.grid.humans(pos))
        zomCasualties = ceil(zomPercent * self.grid.zombies(pos))
        self.grid.destroy(humCasualties, zomCasualties, pos)

        print "after"
        self.grid.printSquare(pos)

