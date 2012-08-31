"""The Critter's behavior."""

import logging
import threading
import time

logging.basicConfig(format='[%(asctime)s][%(threadName)28s][%(levelname)8s] - %(message)s')

class CritterBehavior(threading.Thread):
    """The Critter's behavior.

    Attributes:
        mCritter: The critter.
        mLogger:  The logger.

    """

    def __init__(self, aCritter):
        """Initializes the Critter's behavior.

        Arguments:
            aCritter The critter.

        """
        self.mCritter = aCritter

        self.mLogger = logging.getLogger('CritterBehavior')
        self.mLogger.setLevel(self.mCritter.mSettings.get('logging', 'level'))

        threading.Thread.__init__(self, name='CritterBehavior')

    def run(self):
        """Starts the behavior.

        All decisions are taken here.

        """
        # TODO: Add synchronization with all rites here.

        while True:
            self.mLogger.debug("The behavior starts.")

            # TODO: Jealous class.
            self.mLogger.debug("The number of known critters is: %s." %
                self.mCritter.mRites["Registry"].getNumberOfKnownCritters())

            time.sleep(self.mCritter.mSettings.get('heartbeat', 'period'))

            self.mLogger.debug("The behavior ends.")
