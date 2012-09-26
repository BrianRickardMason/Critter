"""The message processor of a rite.

Receives messages from other parties and handles them in order of appearance.

"""

import logging
import threading

from Queue import PriorityQueue

class MessageProcessor(threading.Thread):
    """The message processor of the a rite.

    Attributes:
        mRite:   The rite.
        mLogger: The logger.
        mQueue:  The queue of messages.

    """

    def __init__(self, aRite):
        """Initializes the message processor.

        Arguments:
            aRite: The rite.

        """
        # Configuring the logger.
        self.mLogger = logging.getLogger(self.__class__.__name__)
        self.mLogger.propagate = False
        handler = logging.FileHandler('/tmp/' + aRite.mCritter.mCrittnick + '.log')
        formatter = logging.Formatter('[%(asctime)s][%(threadName)28s][%(levelname)8s] - %(message)s')
        handler.setFormatter(formatter)
        self.mLogger.addHandler(handler)
        self.mLogger.setLevel(aRite.mCritter.mSettings.get('logging', 'level'))

        self.mRite = aRite

        self.mQueue = PriorityQueue()

        threading.Thread.__init__(self, name=aRite.mRiteName + 'MessageProcessor')

    def run(self):
        """Starts the main loop of the message processor.

        Gets a message from the queue of messages and handle it.

        """
        while True:
            self.mLogger.debug("Waiting for a message.")
            message = self.mQueue.get()[1]

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
