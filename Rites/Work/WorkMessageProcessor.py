import Rites.RiteCommon

from Rites.MessageProcessor  import MessageProcessor
from Rites.Work.WorkCommands import WorkCommandLoadWorkDetails
from Rites.Work.WorkCommands import WorkCommand_Handle_Command_DetermineWorkCycle_Res
from Rites.Work.WorkCommands import WorkCommand_Handle_Command_ExecuteWork_Req

# TODO: If ExecuteWork cannot be executed for whatever reason - inform the sender.
class WorkMessageProcessor(MessageProcessor):
    def __init__(self, aRite):
        MessageProcessor.__init__(self, aRite)

    def processMessage(self, aMessage):
        command = None

        if False: pass
        elif aMessage.messageName == 'Command_DetermineWorkCycle_Res': command = WorkCommand_Handle_Command_DetermineWorkCycle_Res(aMessage)
        elif aMessage.messageName == 'Command_ExecuteWork_Req':        command = WorkCommand_Handle_Command_ExecuteWork_Req(aMessage)
        elif aMessage.messageName == 'LoadWorkDetailsResponse':        command = WorkCommandLoadWorkDetails(aMessage)

        if command:
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.WORK, command)
        else:
            self.mLogger.debug("Dropping unknown message: %s" % aMessage.messageName)
