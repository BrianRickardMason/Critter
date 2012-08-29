import Rites.RiteCommon

from Rites.Database.DatabaseCommands import DatabaseCommandDetermineGraphCycle
from Rites.Database.DatabaseCommands import DatabaseCommandDetermineWorkCycle
from Rites.Database.DatabaseCommands import DatabaseCommandLoadGraphsAndWorks
from Rites.Database.DatabaseCommands import DatabaseCommandLoadWorkDetails
from Rites.MessageProcessor          import MessageProcessor

class DatabaseMessageProcessor(MessageProcessor):
    def __init__(self, aRite):
        MessageProcessor.__init__(self, aRite)

    def processMessage(self, aMessage):
        if aMessage.messageName == 'DetermineGraphCycleRequest':
            command = DatabaseCommandDetermineGraphCycle(aMessage)
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.DATABASE, command)

        elif aMessage.messageName == 'DetermineWorkCycleRequest':
            command = DatabaseCommandDetermineWorkCycle(aMessage)
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.DATABASE, command)

        elif aMessage.messageName == 'LoadGraphAndWorkRequest':
            command = DatabaseCommandLoadGraphsAndWorks(aMessage)
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.DATABASE, command)

        elif aMessage.messageName == 'LoadWorkDetailsRequest':
            command = DatabaseCommandLoadWorkDetails(aMessage)
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.DATABASE, command)

        else:
            self.mLogger.debug("Dropping unknown message: %s" % aMessage.messageName)
