"""The HelloCritty main."""

import sys

from Critter.Critter import Critter

if __name__ == "__main__":
    critter = Critter('HelloCritty', sys.argv[1], ['Poke'])
    critter.run()
