"""The Balancer main."""

import sys

from Critter.Critter import Critter

if __name__ == "__main__":
    critter = Critter('Balancer', sys.argv[1], ['Balance'])
    critter.run()
