"""The message processor of balance rite."""

import Rites.RiteCommon

from Rites.MessageProcessor import MessageProcessor

class BalanceMessageProcessor(MessageProcessor):
    """The message processor of the balance rite."""

    def __init__(self, aRite, aCritterData, aPostOffice):
        """Initializes the message processor.

        Arguments:
            aRite:        The rite.
            aCritterData: The critter data.
            aPostOffice:  The post office.

        """
        MessageProcessor.__init__(self, aRite, aCritterData, aPostOffice, Rites.RiteCommon.BALANCE)

    def processMessage(self, aMessage):
        """Processes the message.

        Arguments:
            aMessage: The message.

        """
        if aMessage.sender.nick == self.mCritterData.mNick:
            self.mLogger.debug("Dropping critter's own message: %s." % aMessage.messageName)

        elif aMessage.messageName == 'CommandWorkExecutionAnnouncement':
            # TODO: Start here.
            pass

        else:
            self.mLogger.debug("Dropping unknown message: %s" % aMessage.messageName)
