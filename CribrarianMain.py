"""The Cribrarian main."""

import sys

from Critter.Critter import Critter

if __name__ == "__main__":
    critter = Critter('Cribrarian', sys.argv[1], ['Database'])
    critter.run()
