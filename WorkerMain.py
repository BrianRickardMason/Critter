"""The Worker main."""

import sys

from Critter.Critter import Critter

if __name__ == "__main__":
    critter = Critter('Worker', sys.argv[1], [])
    critter.run()
