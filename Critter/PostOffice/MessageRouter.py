"""The message router."""

import logging
import threading

logging.basicConfig(format='[%(asctime)s][%(threadName)28s][%(levelname)8s] - %(message)s')

class MessageRouter(threading.Thread):
    """The router of received messages.

    Attributes:
        mCritterData: The critter data.
        mLogger:      The logger.
        mPostOffice:  The post office.

    """

    def __init__(self, aCritterData, aPostOffice):
        """Initializes the message router.

        Arguments:
            aCritterData: The critter data.
            aPostOffice:  The post office.

        """
        self.mLogger = logging.getLogger('MessageRouter')
        self.mLogger.setLevel(logging.INFO)

        self.mCritterData = aCritterData

        self.mPostOffice = aPostOffice

        threading.Thread.__init__(self, name='MessageRouter')

    def run(self):
        """Starts the main loop of the message router."""
        while True:
            message = self.mPostOffice.getIncomingAnnouncement()

            # Forward the message to the rites.
            for key in self.mPostOffice.mCritter.mRites.iterkeys():
                self.mPostOffice.putMessage(key, message)
