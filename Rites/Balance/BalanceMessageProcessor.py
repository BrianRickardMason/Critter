"""The message processor of balance rite."""

import Rites.RiteCommon

from Rites.Balance.BalanceCommands import BalanceCommandCommandWorkExecution
from Rites.MessageProcessor        import MessageProcessor

class BalanceMessageProcessor(MessageProcessor):
    """The message processor of the balance rite."""

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
        if aMessage.sender.nick == self.mRite.mCritterData.mNick:
            self.mLogger.debug("Dropping critter's own message: %s." % aMessage.messageName)

        elif aMessage.messageName == 'CommandWorkExecutionAnnouncement':
            command = BalanceCommandCommandWorkExecution(aMessage)
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.BALANCE, command)

        else:
            self.mLogger.debug("Dropping unknown message: %s" % aMessage.messageName)
