from math import ceil
from random import randint

class Controller:
    def __init__(self):
        return

    def airstrike(self, pos, data, resources):
        # launch an airstrike on a tile
        if resources.airstrikes >= 1:
            print "Airstrike at: " + str(pos)

            humPercent = float(randint(0, 30)) / 100.0
            zomPercent = float(randint(40, 80)) / 100.0

            humCasualties = ceil(humPercent * data.humans(pos))
            zomCasualties = ceil(zomPercent * data.zombies(pos))
            data.destroy(humCasualties, zomCasualties, pos)

            resources.airstrikes -= 1
        else:
            print "No more airstrikes available."
