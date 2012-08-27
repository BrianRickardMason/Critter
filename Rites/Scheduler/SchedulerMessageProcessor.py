"""The message processor of scheduler rite."""

import Rites.RiteCommon

from Rites.MessageProcessor            import MessageProcessor
from Rites.Scheduler.SchedulerCommands import SchedulerCommand_Handle_ExecuteGraphSeekVolunteers
from Rites.Scheduler.SchedulerCommands import SchedulerCommand_Handle_ExecuteGraphVoluntee

class SchedulerMessageProcessor(MessageProcessor):
    """The message processor of the scheduler rite."""

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
        if aMessage.messageName == 'ExecuteGraphSeekVolunteers':
            command = SchedulerCommand_Handle_ExecuteGraphSeekVolunteers(aMessage)
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.SCHEDULER, command)

        elif aMessage.messageName == 'ExecuteGraphVoluntee':
            command = SchedulerCommand_Handle_ExecuteGraphVoluntee(aMessage)
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.SCHEDULER, command)

        else:
            self.mLogger.debug("Dropping unknown message: %s" % aMessage.messageName)
