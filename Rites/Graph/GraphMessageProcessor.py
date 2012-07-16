"""The message processor of graph rite."""

import Rites.RiteCommon

from Rites.Graph.GraphCommands import GraphCommandInitializeGraphExecution
from Rites.Graph.GraphCommands import GraphCommandLoadGraphAndWork
from Rites.Graph.GraphCommands import GraphCommandMarkFinishedWork
from Rites.Graph.GraphCommands import GraphCommandSpawnGraphExecution
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
        if aMessage.sender.nick == self.mRite.mCritterData.mNick:
            self.mLogger.debug("Dropping critter's own message: %s." % aMessage.messageName)

        elif aMessage.messageName == 'DetermineGraphCycleResponse':
            command = GraphCommandSpawnGraphExecution(aMessage)
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.GRAPH, command)

        elif aMessage.messageName == 'ExecuteGraphAnnouncement':
            # TODO: This message should not be processed before all graphs are loaded in Rite.
            command = GraphCommandInitializeGraphExecution(aMessage)
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.GRAPH, command)

        elif aMessage.messageName == 'LoadGraphAndWorkResponse':
            command = GraphCommandLoadGraphAndWork(aMessage)
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.GRAPH, command)

        elif aMessage.messageName == 'ReportFinishedWorkAnnouncement':
            command = GraphCommandMarkFinishedWork(aMessage)
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.GRAPH, command)

        else:
            self.mLogger.debug("Dropping unknown message: %s" % aMessage.messageName)
