import Rites.RiteCommon

from Rites.Graph.GraphCommands import GraphCommandLoadGraphAndWork
from Rites.Graph.GraphCommands import GraphCommandMarkFinishedWork
from Rites.Graph.GraphCommands import GraphCommandSpawnGraphExecution
from Rites.Graph.GraphCommands import GraphCommand_Handle_CommandWorkExecutionSeekVolunteers
from Rites.Graph.GraphCommands import GraphCommand_Handle_CommandWorkExecutionSelectVolunteer
from Rites.Graph.GraphCommands import GraphCommand_Handle_CommandWorkExecutionVoluntee
from Rites.Graph.GraphCommands import GraphCommand_Handle_Command_Req_ExecuteGraph
from Rites.Graph.GraphCommands import GraphCommand_Handle_Command_Res_Election
from Rites.Graph.GraphCommands import GraphCommand_Handle_ExecuteGraphSeekVolunteers
from Rites.Graph.GraphCommands import GraphCommand_Handle_ExecuteGraphSelectVolunteer
from Rites.MessageProcessor    import MessageProcessor

class GraphMessageProcessor(MessageProcessor):
    def __init__(self, aRite):
        MessageProcessor.__init__(self, aRite)

    def processMessage(self, aMessage):
        command = None

        if   aMessage.messageName == 'CommandWorkExecutionSeekVolunteers':  command = GraphCommand_Handle_CommandWorkExecutionSeekVolunteers(aMessage)
        elif aMessage.messageName == 'CommandWorkExecutionSelectVolunteer': command = GraphCommand_Handle_CommandWorkExecutionSelectVolunteer(aMessage)
        elif aMessage.messageName == 'CommandWorkExecutionVoluntee':        command = GraphCommand_Handle_CommandWorkExecutionVoluntee(aMessage)
        elif aMessage.messageName == 'Command_Req_ExecuteGraph':            command = GraphCommand_Handle_Command_Req_ExecuteGraph(aMessage)
        elif aMessage.messageName == 'Command_Res_Election':                command = GraphCommand_Handle_Command_Res_Election(aMessage)
        elif aMessage.messageName == 'DetermineGraphCycleResponse':         command = GraphCommandSpawnGraphExecution(aMessage)
        elif aMessage.messageName == 'ExecuteGraphSeekVolunteers':          command = GraphCommand_Handle_ExecuteGraphSeekVolunteers(aMessage)
        elif aMessage.messageName == 'ExecuteGraphSelectVolunteer':         command = GraphCommand_Handle_ExecuteGraphSelectVolunteer(aMessage)
        elif aMessage.messageName == 'LoadGraphAndWorkResponse':            command = GraphCommandLoadGraphAndWork(aMessage)
        elif aMessage.messageName == 'ReportFinishedWorkAnnouncement':      command = GraphCommandMarkFinishedWork(aMessage)

        if command:
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.GRAPH, command)
        else:
            self.mLogger.debug("Dropping unknown message: %s." % aMessage.messageName)
