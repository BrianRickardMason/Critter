"""The message processor of database rite."""

import Rites.RiteCommon

from Rites.Database.DatabaseCommands import DatabaseCommandDetermineGraphCycle
from Rites.Database.DatabaseCommands import DatabaseCommandDetermineWorkCycle
from Rites.Database.DatabaseCommands import DatabaseCommandLoadGraphsAndWorks
from Rites.Database.DatabaseCommands import DatabaseCommandLoadWorkDetails
from Rites.MessageProcessor          import MessageProcessor

class DatabaseMessageProcessor(MessageProcessor):
    """The message processor of the database rite."""

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
