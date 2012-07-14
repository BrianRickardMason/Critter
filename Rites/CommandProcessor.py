"""The command processor of a rite.

Receives commands from other parties and executes them in order of appearance.

"""

import logging
import threading

from Queue import Queue

logging.basicConfig(format='[%(asctime)s][%(threadName)28s][%(levelname)8s] - %(message)s')

class CommandProcessor(threading.Thread):
    """The command processor of a rite.

    Attributes:
        mRite:        The rite.
        mCritterData: The critter data.
        mPostOffice:  The post office.
        mLogger:      The logger.
        mQueue:       The queue of commands.

    """

    def __init__(self, aRite, aCritterData, aPostOffice, aRiteName):
        """Initializes the command processor.

        Arguments:
            aRite:        The rite.
            aCritterData: The critter data.
            aPostOffice:  The post office.
            aRiteName:    The rite name.

        """
        self.mLogger = logging.getLogger(aRiteName + 'CommandProcessor')
        self.mLogger.setLevel(logging.INFO)

        self.mRite = aRite

        self.mCritterData = aCritterData
        self.mPostOffice  = aPostOffice

        self.mQueue = Queue()

        threading.Thread.__init__(self, name=aRiteName + 'CommandProcessor')

    def run(self):
        """Starts the main loop of the command processor.

        Gets a command from the queue of commands and executes it.

        """
        while True:
            self.mLogger.debug("Waiting for a command.")
            command = self.mQueue.get()
            self.mLogger.debug("Executing a command: %s." % command.mName)
            command.execute(self)

    def put(self, aCommand):
        """Puts a command into the queue.

        Arguments:
            aCommand The command.

        """
        self.mQueue.put(aCommand)
