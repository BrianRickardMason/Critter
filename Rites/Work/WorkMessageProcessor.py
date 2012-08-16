"""The message processor of balance rite."""

import Rites.RiteCommon

from Rites.MessageProcessor  import MessageProcessor
from Rites.Work.WorkCommands import WorkCommandInitializeWorkExecution
from Rites.Work.WorkCommands import WorkCommandSpawnWorkExecution

class WorkMessageProcessor(MessageProcessor):
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

        elif aMessage.messageName == 'DetermineWorkCycleResponse':
            command = WorkCommandSpawnWorkExecution(aMessage)
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.WORK, command)

        elif aMessage.messageName == 'ExecuteWorkAnnouncement':
            # FIXME: Should only be executed by receiver!
            # TODO:  If cannot be executed for whatever reason - inform the sender.
            command = WorkCommandInitializeWorkExecution(aMessage)
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.WORK, command)

        else:
            self.mLogger.debug("Dropping unknown message: %s" % aMessage.messageName)
