"""The message processor of database rite."""

import Rites.RiteCommon

from Rites.Database.DatabaseCommands import DatabaseCommandDetermineGraphCycle
from Rites.Database.DatabaseCommands import DatabaseCommandFoo
from Rites.Database.DatabaseCommands import DatabaseCommandLoadGraphsAndWorks
from Rites.MessageProcessor          import MessageProcessor

class DatabaseMessageProcessor(MessageProcessor):
    """The message processor of the database rite."""

    def __init__(self, aRite, aCritterData, aPostOffice):
        """Initializes the message processor.

        Arguments:
            aRite:        The rite.
            aCritterData: The critter data.
            aPostOffice:  The post office.

        """
        MessageProcessor.__init__(self, aRite, aCritterData, aPostOffice, Rites.RiteCommon.DATABASE)

    def processMessage(self, aMessage):
        """Processes the message.

        Arguments:
            aMessage: The message.

        """
        if aMessage.sender.nick == self.mCritterData.mNick:
            self.mLogger.debug("Dropping critter's own message: %s." % aMessage.messageName)

        elif aMessage.messageName == 'DetermineGraphCycleRequest':
            command = DatabaseCommandDetermineGraphCycle(aMessage)
            self.mPostOffice.putCommand(Rites.RiteCommon.DATABASE, command)

        elif aMessage.messageName == 'ExecuteGraphAnnouncement':
            command = DatabaseCommandFoo()
            self.mPostOffice.putCommand(Rites.RiteCommon.DATABASE, command)

        elif aMessage.messageName == 'LoadGraphAndWorkRequest':
            command = DatabaseCommandLoadGraphsAndWorks(aMessage)
            self.mPostOffice.putCommand(Rites.RiteCommon.DATABASE, command)

        else:
            self.mLogger.debug("Dropping unknown message: %s" % aMessage.messageName)
