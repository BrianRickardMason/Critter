"""The GraphYeeti main."""

import sys

from Critter.Critter import Critter

if __name__ == "__main__":
    critter = Critter('GraphYeeti', sys.argv[1], ['Graph'])
    critter.run()
