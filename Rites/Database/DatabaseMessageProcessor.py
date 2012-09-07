import Rites.RiteCommon

from Rites.Database.DatabaseCommands import DatabaseCommand_Handle_Command_DetermineGraphCycle_Req
from Rites.Database.DatabaseCommands import DatabaseCommand_Handle_Command_DetermineWorkCycle_Req
from Rites.Database.DatabaseCommands import DatabaseCommand_Handle_Command_Election_Req
from Rites.Database.DatabaseCommands import DatabaseCommand_Handle_Command_LoadGraphAndWork_Req
from Rites.Database.DatabaseCommands import DatabaseCommand_Handle_Command_LoadGraphDetails_Req
from Rites.Database.DatabaseCommands import DatabaseCommand_Handle_Command_LoadWorkDetails_Req
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
        elif aMessage.messageName == 'Command_LoadGraphAndWork_Req':    command = DatabaseCommand_Handle_Command_LoadGraphAndWork_Req(aMessage)
        elif aMessage.messageName == 'Command_LoadGraphDetails_Req':    command = DatabaseCommand_Handle_Command_LoadGraphDetails_Req(aMessage)
        elif aMessage.messageName == 'Command_LoadWorkDetails_Req':     command = DatabaseCommand_Handle_Command_LoadWorkDetails_Req(aMessage)

        if command:
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.DATABASE, command)
        else:
            self.mLogger.debug("Dropping unknown message: %s" % aMessage.messageName)
