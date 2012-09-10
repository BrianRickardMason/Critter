"""The rite."""

import logging
import threading

from Rites.CommandProcessor import CommandProcessor

logging.basicConfig(format='[%(asctime)s][%(threadName)28s][%(levelname)8s] - %(message)s')

class Rite(threading.Thread):
    """The graph rite.

    Attributes:
        mCritter:    The critter.
        mRiteName:   The name of the rite.
        mSettings:   The settings.
        mPostOffice: The post office.
        mLogger:     The logger.

    """

    def __init__(self, aCritter, aSettings, aPostOffice, aRiteName, aMessageProcessorType):
        """Initializes the rite.

        Arguments:
            aCritter:              The critter.
            aSettings:             The settings.
            aPostOffice:           The post office.
            aRiteName:             The name of the rite.
            aMessageProcessorType: The type of the command processor.

        """
        self.mSettings = aSettings

        self.mLogger = logging.getLogger(aRiteName + 'Rite')
        self.mLogger.setLevel(self.mSettings.get('logging', 'level'))

        self.mCritter     = aCritter
        self.mPostOffice  = aPostOffice
        self.mRiteName    = aRiteName

        self.mLogger.info("Spawning the command processor.")
        self.mCommandProcessor = CommandProcessor(self)
        self.mCommandProcessor.setDaemon(True)
        self.mCommandProcessor.start()

        self.mLogger.info("Spawning the message processor.")
        self.mMessageProcessor = aMessageProcessorType(self)
        self.mMessageProcessor.setDaemon(True)
        self.mMessageProcessor.start()

        threading.Thread.__init__(self, name=aRiteName + 'Rite')

    def run(self):
        """Starts the main loop of the rite."""
        raise NotImplementedError

    def putCommand(self, aCommand):
        """Puts a command into the queue of command processor.

        Arguments:
            aCommand The command.

        """
        self.mCommandProcessor.put(aCommand)

    def putMessage(self, aMessage):
        """Puts a message into the queue of message processor.

        Arguments:
            aMessage The message.

        """
        self.mMessageProcessor.put(aMessage)
