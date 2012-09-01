import Rites.RiteCommon

from Rites.MessageProcessor  import MessageProcessor
from Rites.Work.WorkCommands import WorkCommand_Handle_Command_Req_ExecuteWork
from Rites.Work.WorkCommands import WorkCommand_Handle_Command_Res_DetermineWorkCycle
from Rites.Work.WorkCommands import WorkCommandInitializeWorkExecution
from Rites.Work.WorkCommands import WorkCommandLoadWorkDetails
from Rites.Work.WorkCommands import WorkCommandSpawnWorkExecution

# TODO: If ExecuteWork cannot be executed for whatever reason - inform the sender.
class WorkMessageProcessor(MessageProcessor):
    def __init__(self, aRite):
        MessageProcessor.__init__(self, aRite)

    def processMessage(self, aMessage):
        command = None

        if False: pass
        elif aMessage.messageName == 'Command_Req_ExecuteWork':        command = WorkCommand_Handle_Command_Req_ExecuteWork(aMessage)
        elif aMessage.messageName == 'Command_Res_DetermineWorkCycle': command = WorkCommand_Handle_Command_Res_DetermineWorkCycle(aMessage)
        elif aMessage.messageName == 'DetermineWorkCycleResponse':     command = WorkCommandSpawnWorkExecution(aMessage)
        elif aMessage.messageName == 'ExecuteWorkAnnouncement':        command = WorkCommandInitializeWorkExecution(aMessage)
        elif aMessage.messageName == 'LoadWorkDetailsResponse':        command = WorkCommandLoadWorkDetails(aMessage)

        if command:
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.WORK, command)
        else:
            self.mLogger.debug("Dropping unknown message: %s" % aMessage.messageName)
