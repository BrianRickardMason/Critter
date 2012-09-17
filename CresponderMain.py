import sys

from Critter.Critter import Critter

class Cresponder(Critter):
    def __init__(self, aCrittnick, aRites):
        Critter.__init__(self, aCrittnick , aCrittnick, aRites)

if __name__ == "__main__":
    critter = Cresponder(sys.argv[1], [])
    critter.run()
