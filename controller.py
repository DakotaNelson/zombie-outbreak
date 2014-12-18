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

            data.destroyPercent(humPercent, zomPercent, pos)
            data.neighborDestroyPercent(humPercent, zomPercent, pos)

            resources.airstrikes -= 1
        else:
            print "No more airstrikes available."

    def infantry(self, pos, data, resources):
        #send the marines!
        if resources.infantry >= 1:
            print "Militia at: " + str(pos)

            data.destroy(0, 200, pos)
            data.add(50, 0, pos)

            resources.infantry -= 50
        else:
            print "No militia left."
