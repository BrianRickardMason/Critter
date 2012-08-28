"""The message processor of graph rite."""

import Rites.RiteCommon

from Rites.Graph.GraphCommands import GraphCommandLoadGraphAndWork
from Rites.Graph.GraphCommands import GraphCommandMarkFinishedWork
from Rites.Graph.GraphCommands import GraphCommandSpawnGraphExecution
from Rites.Graph.GraphCommands import GraphCommand_Handle_CommandWorkExecutionSeekVolunteers
from Rites.Graph.GraphCommands import GraphCommand_Handle_CommandWorkExecutionVoluntee
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
        command = None

        if aMessage.messageName == 'CommandWorkExecutionSeekVolunteers': command = GraphCommand_Handle_CommandWorkExecutionSeekVolunteers(aMessage)
        if aMessage.messageName == 'CommandWorkExecutionVoluntee':       command = GraphCommand_Handle_CommandWorkExecutionVoluntee(aMessage)
        if aMessage.messageName == 'DetermineGraphCycleResponse':        command = GraphCommandSpawnGraphExecution(aMessage)
        if aMessage.messageName == 'ExecuteGraphSeekVolunteers':         command = GraphCommand_Handle_ExecuteGraphSeekVolunteers(aMessage)
        if aMessage.messageName == 'ExecuteGraphSelectVolunteer':        command = GraphCommand_Handle_ExecuteGraphSelectVolunteer(aMessage)
        if aMessage.messageName == 'LoadGraphAndWorkResponse':           command = GraphCommandLoadGraphAndWork(aMessage)
        if aMessage.messageName == 'ReportFinishedWorkAnnouncement':     command = GraphCommandMarkFinishedWork(aMessage)

        if command:
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.GRAPH, command)
        else:
            self.mLogger.debug("Dropping unknown message: %s" % aMessage.messageName)
