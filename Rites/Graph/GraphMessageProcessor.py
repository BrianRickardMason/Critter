import Rites.RiteCommon

from Rites.Graph.GraphCommands import GraphCommand_Handle_Command_DetermineGraphCycle_Res
from Rites.Graph.GraphCommands import GraphCommand_Handle_Command_Election_Res
from Rites.Graph.GraphCommands import GraphCommand_Handle_Command_ExecuteGraph_Req
from Rites.Graph.GraphCommands import GraphCommand_Handle_Command_LoadGraphAndWork_Res
from Rites.Graph.GraphCommands import GraphCommand_Handle_Command_LoadGraphDetails_Res
from Rites.Graph.GraphCommands import GraphCommand_Handle_Command_LoadWorkDetails_Res
from Rites.Graph.GraphCommands import GraphCommand_Handle_Command_OrderWorkExecution_Res
from Rites.MessageProcessor    import MessageProcessor

class GraphMessageProcessor(MessageProcessor):
    def __init__(self, aRite):
        MessageProcessor.__init__(self, aRite)

    def processMessage(self, aMessage):
        command = None

        if aMessage.messageName == 'Command_DetermineGraphCycle_Res':
            command = GraphCommand_Handle_Command_DetermineGraphCycle_Res(aMessage)
        elif aMessage.messageName == 'Command_Election_Res':
            command = GraphCommand_Handle_Command_Election_Res(aMessage)
        elif aMessage.messageName == 'Command_ExecuteGraph_Req':
            command = GraphCommand_Handle_Command_ExecuteGraph_Req(aMessage)
        elif aMessage.messageName == 'Command_LoadGraphAndWork_Res':
            command = GraphCommand_Handle_Command_LoadGraphAndWork_Res(aMessage)
        elif aMessage.messageName == 'Command_LoadGraphDetails_Res':
            command = GraphCommand_Handle_Command_LoadGraphDetails_Res(aMessage)
        elif aMessage.messageName == 'Command_LoadWorkDetails_Res':
            command = GraphCommand_Handle_Command_LoadWorkDetails_Res(aMessage)
        elif aMessage.messageName == 'Command_OrderWorkExecution_Res':
            command = GraphCommand_Handle_Command_OrderWorkExecution_Res(aMessage)

        if command:
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.GRAPH, command)
        else:
            self.mLogger.debug("Dropping unknown message: %s." % aMessage.messageName)
