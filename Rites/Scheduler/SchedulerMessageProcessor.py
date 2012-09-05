import Rites.RiteCommon

from Rites.Scheduler.SchedulerCommands import SchedulerCommand_Handle_Command_ExecuteGraph_Res
from Rites.Scheduler.SchedulerCommands import SchedulerCommand_Handle_Command_LoadGraphDetails_Res
from Rites.MessageProcessor            import MessageProcessor

class SchedulerMessageProcessor(MessageProcessor):
    def __init__(self, aRite):
        MessageProcessor.__init__(self, aRite)

    def processMessage(self, aMessage):
        command = None

        if aMessage.messageName == 'Command_ExecuteGraph_Res':
            command = SchedulerCommand_Handle_Command_ExecuteGraph_Res(aMessage)
        elif aMessage.messageName == 'Command_LoadGraphDetails_Res':
            command = SchedulerCommand_Handle_Command_LoadGraphDetails_Res(aMessage)

        if command:
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.SCHEDULER, command)
        else:
            self.mLogger.debug("Dropping unknown message: %s." % aMessage.messageName)
