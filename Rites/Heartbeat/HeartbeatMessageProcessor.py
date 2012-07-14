"""The message processor of heartbeat rite."""

import Rites.RiteCommon

from Rites.MessageProcessor import MessageProcessor

class HeartbeatMessageProcessor(MessageProcessor):
    """The message processor of the heartbeat rite."""

    def __init__(self, aRite, aCritterData, aPostOffice):
        """Initializes the message processor.

        Arguments:
            aRite:        The rite.
            aCritterData: The critter data.
            aPostOffice:  The post office.

        """
        MessageProcessor.__init__(self, aRite, aCritterData, aPostOffice, Rites.RiteCommon.HEARTBEAT)

    def processMessage(self, aMessage):
        """Processes the message.

        Arguments:
            aMessage: The message.

        """
        self.mLogger.debug("Dropping unknown message: %s" % aMessage.messageName)
