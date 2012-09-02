import Rites.RiteCommon

from Rites.Database.DatabaseCommands import DatabaseCommandLoadGraphsAndWorks
from Rites.Database.DatabaseCommands import DatabaseCommandLoadWorkDetails
from Rites.Database.DatabaseCommands import DatabaseCommand_Handle_Command_DetermineGraphCycle_Req
from Rites.Database.DatabaseCommands import DatabaseCommand_Handle_Command_DetermineWorkCycle_Req
from Rites.Database.DatabaseCommands import DatabaseCommand_Handle_Command_Election_Req
from Rites.MessageProcessor          import MessageProcessor

class DatabaseMessageProcessor(MessageProcessor):
    def __init__(self, aRite):
        MessageProcessor.__init__(self, aRite)

    def processMessage(self, aMessage):
        command = None

        if False: pass
        elif aMessage.messageName == 'Command_DetermineGraphCycle_Req': command = DatabaseCommand_Handle_Command_DetermineGraphCycle_Req(aMessage)
        elif aMessage.messageName == 'Command_DetermineWorkCycle_Req':  command = DatabaseCommand_Handle_Command_DetermineWorkCycle_Req(aMessage)
        elif aMessage.messageName == 'Command_Election_Req':            command = DatabaseCommand_Handle_Command_Election_Req(aMessage)
        elif aMessage.messageName == 'LoadGraphAndWorkRequest':         command = DatabaseCommandLoadGraphsAndWorks(aMessage)
        elif aMessage.messageName == 'LoadWorkDetailsRequest':          command = DatabaseCommandLoadWorkDetails(aMessage)

        if command:
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.DATABASE, command)
        else:
            self.mLogger.debug("Dropping unknown message: %s" % aMessage.messageName)
