import Rites.RiteCommon

from Rites.Graph.GraphCommands import GraphCommand_Handle_Command_Req_ExecuteGraph
from Rites.Graph.GraphCommands import GraphCommand_Handle_Command_Res_Election
from Rites.Graph.GraphCommands import GraphCommand_Handle_LoadGraphAndWorkResponse
from Rites.MessageProcessor    import MessageProcessor

class GraphMessageProcessor(MessageProcessor):
    def __init__(self, aRite):
        MessageProcessor.__init__(self, aRite)

    def processMessage(self, aMessage):
        command = None

        if False: pass
        elif aMessage.messageName == 'Command_Req_ExecuteGraph': command = GraphCommand_Handle_Command_Req_ExecuteGraph(aMessage)
        elif aMessage.messageName == 'Command_Res_Election':     command = GraphCommand_Handle_Command_Res_Election(aMessage)
        elif aMessage.messageName == 'LoadGraphAndWorkResponse': command = GraphCommand_Handle_LoadGraphAndWorkResponse(aMessage)

        if command:
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.GRAPH, command)
        else:
            self.mLogger.debug("Dropping unknown message: %s." % aMessage.messageName)
