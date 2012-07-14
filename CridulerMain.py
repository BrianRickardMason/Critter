"""The Criduler main."""

import sys

from Critter.Critter import Critter

if __name__ == "__main__":
    critter = Critter('Criduler', sys.argv[1], ['Scheduler'])
    critter.run()
