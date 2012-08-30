import Rites.RiteCommon

from Rites.Database.DatabaseCommands import DatabaseCommandDetermineGraphCycle
from Rites.Database.DatabaseCommands import DatabaseCommandDetermineWorkCycle
from Rites.Database.DatabaseCommands import DatabaseCommandLoadGraphsAndWorks
from Rites.Database.DatabaseCommands import DatabaseCommandLoadWorkDetails
from Rites.Database.DatabaseCommands import DatabaseCommand_Handle_Command_Req_DetermineGraphCycle
from Rites.Database.DatabaseCommands import DatabaseCommand_Handle_Command_Req_Election
from Rites.MessageProcessor          import MessageProcessor

class DatabaseMessageProcessor(MessageProcessor):
    def __init__(self, aRite):
        MessageProcessor.__init__(self, aRite)

    def processMessage(self, aMessage):
        command = None

        if False: pass
        elif aMessage.messageName == 'Command_Req_DetermineGraphCycle': command = DatabaseCommand_Handle_Command_Req_DetermineGraphCycle(aMessage)
        elif aMessage.messageName == 'Command_Req_Election':            command = DatabaseCommand_Handle_Command_Req_Election(aMessage)
        elif aMessage.messageName == 'DetermineGraphCycleRequest':      command = DatabaseCommandDetermineGraphCycle(aMessage)
        elif aMessage.messageName == 'DetermineWorkCycleRequest':       command = DatabaseCommandDetermineWorkCycle(aMessage)
        elif aMessage.messageName == 'LoadGraphAndWorkRequest':         command = DatabaseCommandLoadGraphsAndWorks(aMessage)
        elif aMessage.messageName == 'LoadWorkDetailsRequest':          command = DatabaseCommandLoadWorkDetails(aMessage)

        if command:
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.DATABASE, command)
        else:
            self.mLogger.debug("Dropping unknown message: %s" % aMessage.messageName)
