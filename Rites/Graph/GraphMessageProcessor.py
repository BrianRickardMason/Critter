"""The message processor of graph rite."""

import Rites.RiteCommon

from Rites.Graph.GraphCommands import GraphCommandLoadGraphAndWork
from Rites.Graph.GraphCommands import GraphCommandMarkFinishedWork
from Rites.Graph.GraphCommands import GraphCommandSpawnGraphExecution
from Rites.Graph.GraphCommands import GraphCommand_Handle_CommandWorkExecutionSeekVolunteers
from Rites.Graph.GraphCommands import GraphCommand_Handle_ExecuteGraphSeekVolunteers
from Rites.Graph.GraphCommands import GraphCommand_Handle_ExecuteGraphSelectVolunteer
from Rites.MessageProcessor    import MessageProcessor

class GraphMessageProcessor(MessageProcessor):
    """The message processor of the graph rite."""

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
        if aMessage.messageName == 'DetermineGraphCycleResponse':
            # TODO: This should not be done here.
            if aMessage.sender.nick == self.mRite.mCritterData.mNick:
                self.mLogger.debug("Dropping critter's own message: %s." % aMessage.messageName)
                return
            command = GraphCommandSpawnGraphExecution(aMessage)
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.GRAPH, command)

        elif aMessage.messageName == 'ExecuteGraphSeekVolunteers':
            command = GraphCommand_Handle_ExecuteGraphSeekVolunteers(aMessage)
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.GRAPH, command)

        elif aMessage.messageName == 'ExecuteGraphSelectVolunteer':
            command = GraphCommand_Handle_ExecuteGraphSelectVolunteer(aMessage)
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.GRAPH, command)

        elif aMessage.messageName == 'ExecuteGraphSeekVolunteers':
            command = GraphCommand_Handle_CommandWorkExecutionSeekVolunteers(aMessage)
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.GRAPH, command)

        elif aMessage.messageName == 'LoadGraphAndWorkResponse':
            # TODO: This should not be done here.
            if aMessage.sender.nick == self.mRite.mCritterData.mNick:
                self.mLogger.debug("Dropping critter's own message: %s." % aMessage.messageName)
                return
            command = GraphCommandLoadGraphAndWork(aMessage)
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.GRAPH, command)

        elif aMessage.messageName == 'ReportFinishedWorkAnnouncement':
            # TODO: This should not be done here.
            if aMessage.sender.nick == self.mRite.mCritterData.mNick:
                self.mLogger.debug("Dropping critter's own message: %s." % aMessage.messageName)
                return
            command = GraphCommandMarkFinishedWork(aMessage)
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.GRAPH, command)

        else:
            self.mLogger.debug("Dropping unknown message: %s" % aMessage.messageName)
