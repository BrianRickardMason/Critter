"""The message processor of poke rite."""

import Rites.RiteCommon

from Rites.MessageProcessor import MessageProcessor

class PokeMessageProcessor(MessageProcessor):
    """The message processor of the poke rite."""

    def __init__(self, aRite):
        """Initializes the message processor.

        Arguments:
            aRite: The rite.

        """
        MessageProcessor.__init__(self, aRite)

    def processMessage(self, aMessage):
        """Processes the message.

        Arguments:
            aMessage: The message.

        """
        self.mLogger.debug("Dropping unknown message: %s" % aMessage.messageName)
