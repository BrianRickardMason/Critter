import Rites.RiteCommon

from Rites.MessageProcessor            import MessageProcessor
from Rites.Scheduler.SchedulerCommands import SchedulerCommand_Handle_ExecuteGraphSeekVolunteers
from Rites.Scheduler.SchedulerCommands import SchedulerCommand_Handle_ExecuteGraphSelectVolunteer
from Rites.Scheduler.SchedulerCommands import SchedulerCommand_Handle_ExecuteGraphVoluntee

class SchedulerMessageProcessor(MessageProcessor):
    def __init__(self, aRite):
        MessageProcessor.__init__(self, aRite)

    def processMessage(self, aMessage):
        command = None

        if   aMessage.messageName == 'ExecuteGraphSeekVolunteers':  command = SchedulerCommand_Handle_ExecuteGraphSeekVolunteers(aMessage)
        elif aMessage.messageName == 'ExecuteGraphSelectVolunteer': command = SchedulerCommand_Handle_ExecuteGraphSelectVolunteer(aMessage)
        elif aMessage.messageName == 'ExecuteGraphVoluntee':        command = SchedulerCommand_Handle_ExecuteGraphVoluntee(aMessage)

        if command:
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.SCHEDULER, command)
        else:
            self.mLogger.debug("Dropping unknown message: %s" % aMessage.messageName)
