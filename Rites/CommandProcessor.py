"""The command processor of a rite.

Receives commands from other parties and executes them in order of appearance.

"""

import logging
import threading

from Queue import PriorityQueue

class CommandProcessor(threading.Thread):
    """The command processor of a rite.

    Attributes:
        mRite:   The rite.
        mLogger: The logger.
        mQueue:  The queue of commands.

    """

    def __init__(self, aRite):
        """Initializes the command processor.

        Arguments:
            aRite: The rite.

        """
        self.mRite = aRite

        # Configuring the logger.
        self.mLogger = logging.getLogger(aRite.mRiteName + self.__class__.__name__)
        self.mLogger.propagate = False
        handler = logging.FileHandler('/tmp/' + aRite.mCritter.mCrittnick + '.log')
        formatter = logging.Formatter('[%(asctime)s][%(threadName)28s][%(levelname)8s] - %(message)s')
        handler.setFormatter(formatter)
        self.mLogger.addHandler(handler)
        self.mLogger.setLevel(aRite.mCritter.mSettings.get('logging', 'level'))

        self.mQueue = PriorityQueue()

        threading.Thread.__init__(self, name=aRite.mRiteName + 'CommandProcessor')

    def run(self):
        """Starts the main loop of the command processor.

        Gets a command from the queue of commands and executes it.

        """
        while True:
            self.mLogger.debug("Waiting for a command.")
            command = self.mQueue.get()[1]
            self.mLogger.debug("Executing a command: %s." % command.__class__.__name__)
            command.execute(self)

    def put(self, aCommand):
        """Puts a command into the queue.

        Arguments:
            aCommand The command.

        """
        self.mQueue.put(aCommand)
