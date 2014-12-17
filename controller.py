from math import ceil
from random import randint

class Controller:
    def __init__(self, grid):
        return

    def airstrike(self, pos, data):
        # launch an airstrike on a tile
        print "airstrike at: " + str(pos)

        humPercent = float(randint(0, 30)) / 100.0
        zomPercent = float(randint(40, 80)) / 100.0

        humCasualties = ceil(humPercent * data.humans(pos))
        zomCasualties = ceil(zomPercent * data.zombies(pos))
        data.destroy(humCasualties, zomCasualties, pos)

