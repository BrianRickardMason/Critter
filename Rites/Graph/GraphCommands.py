import Rites.RiteCommon

from GraphRiteSession import GraphRiteSession

class GraphCommand_Handle_Command_Res_Election(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        critthash = self.mMessage.critthash

        # There's an active sent command.
        if critthash in aCommandProcessor.mRite.mSentCommands['Command_Req_Election']:
            # Delete the sent command entry.
            del aCommandProcessor.mRite.mSentCommands['Command_Req_Election'][critthash]

        # There's an active election.
        if critthash in aCommandProcessor.mRite.mElections:
            # I am the winner.
            if self.mMessage.crittnick == aCommandProcessor.mRite.mCritter.mCritterData.mNick:
                # Get the election topic.
                message = aCommandProcessor.mRite.mElections[critthash]['message']

                # Handle the election topic.
                if message.messageName == 'Command_Req_ExecuteGraph':
                    command = GraphCommand_Handle_Command_Req_ExecuteGraph_WonElection(message)
                    aCommandProcessor.mRite.mPostOffice.putCommand(Rites.RiteCommon.GRAPH, command)

            # Delete the election entry.
            del aCommandProcessor.mRite.mElections[critthash]

class GraphCommand_Handle_Command_Req_ExecuteGraph(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        critthash = self.mMessage.critthash

        assert critthash not in aCommandProcessor.mRite.mElections, "Not handled yet. Duplicated critthash."
        aCommandProcessor.mRite.mElections[critthash] = {'message':   self.mMessage}

        assert 'Command_Req_Election' in aCommandProcessor.mRite.mSentCommands, "Missing key in the dictionary of sent commands."
        assert critthash not in aCommandProcessor.mRite.mSentCommands['Command_Req_Election'], "Not handled yet. Duplicated critthash."
        aCommandProcessor.mRite.mSentCommands['Command_Req_Election'][critthash] = {'critthash': critthash}
        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            'Command_Req_Election',
            {'messageName': 'Command_Req_Election',
             'critthash':   critthash,
             'crittnick':   aCommandProcessor.mRite.mCritter.mCritterData.mNick}
        )
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

class GraphCommand_Handle_Command_Req_ExecuteGraph_WonElection(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        aCommandProcessor.mLogger.info("TODO: Start from here!")

class GraphCommand_Handle_LoadGraphAndWorkResponse(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        # Store graphs.
        for graph in self.mMessage.graphs:
            aCommandProcessor.mRite.mGraphs.append(graph.graphName)

        # Store works.
        for work in self.mMessage.works:
            if work.graphName not in aCommandProcessor.mRite.mWorks:
                aCommandProcessor.mRite.mWorks[work.graphName] = []

            aCommandProcessor.mRite.mWorks[work.graphName].append(work.workName)

        # Store predecessors.
        for predecessor in self.mMessage.workPredecessors:
            if predecessor.workName not in aCommandProcessor.mRite.mWorkPredecessors:
                aCommandProcessor.mRite.mWorkPredecessors[predecessor.workName] = []

            aCommandProcessor.mRite.mWorkPredecessors[predecessor.workName].append(predecessor.predecessorWorkName)
