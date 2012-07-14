"""The message processor of a rite.

Receives messages from other parties and handles them in order of appearance.

"""

import logging
import threading

from Queue import Queue

logging.basicConfig(format='[%(asctime)s][%(threadName)28s][%(levelname)8s] - %(message)s')

class MessageProcessor(threading.Thread):
    """The message processor of the a rite.

    Attributes:
        mRite:        The rite.
        mCritterData: The critter data.
        mPostOffice:  The post office.
        mLogger:      The logger.
        mQueue:       The queue of messages.

    """

    def __init__(self, aRite, aCritterData, aPostOffice, aRiteName):
        """Initializes the message processor.

        Arguments:
            aRite:        The rite.
            aCritterData: The critter data.
            aPostOffice:  The post office.
            aRiteName:    The rite name.

        """
        self.mLogger = logging.getLogger(aRiteName + 'MessageProcessor')
        self.mLogger.setLevel(logging.INFO)

        self.mRite = aRite

        self.mCritterData = aCritterData
        self.mPostOffice  = aPostOffice

        self.mQueue = Queue()

        threading.Thread.__init__(self, name=aRiteName + 'MessageProcessor')

    def run(self):
        """Starts the main loop of the message processor.

        Gets a message from the queue of messages and handle it.

        """
        while True:
            self.mLogger.debug("Waiting for a message.")
            message = self.mQueue.get()

            self.mLogger.debug("Processing the message: %s." % message.messageName)
            self.processMessage(message)

    def processMessage(self, aMessage):
        """Processes the message.

        Arguments:
            aMessage: The message.

        """
        raise NotImplementedError

    def put(self, aMessage):
        """Puts a message into the queue.

        Arguments:
            aMessage The message.

        """
        self.mQueue.put(aMessage)
