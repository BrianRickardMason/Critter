import os

import Rites.RiteCommon

from GraphRiteSession import GraphRiteSession

class GraphCommand_Handle_Command_ExecuteGraph_Req(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        graphExecutionCritthash = self.mMessage.graphExecutionCritthash

        messageName = self.mMessage.messageName
        assert graphExecutionCritthash not in aCommandProcessor.mRite.mRecvReq[messageName], "Not handled yet. Duplicated critthash."
        aCommandProcessor.mLogger.debug("Insert(ing) the recv request: [%s][%s]." % (messageName, graphExecutionCritthash))
        aCommandProcessor.mRite.mRecvReq[messageName][graphExecutionCritthash] = self.mMessage

        assert graphExecutionCritthash not in aCommandProcessor.mRite.mElections, "Not handled yet. Duplicated critthash."
        aCommandProcessor.mLogger.debug("Insert the election entry: [%s]." % graphExecutionCritthash)
        aCommandProcessor.mRite.mElections[graphExecutionCritthash] = {'message': self.mMessage}

        messageName = 'Command_Election_Req'
        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            messageName,
            {'messageName': messageName,
             'critthash':   graphExecutionCritthash,
             'crittnick':   aCommandProcessor.mRite.mCritter.mCritterData.mNick}
        )
        assert graphExecutionCritthash not in aCommandProcessor.mRite.mSentReq[messageName], "Not handled yet. Duplicated critthash."
        aCommandProcessor.mLogger.debug("Insert the sent request entry: [%s][%s]." % (messageName, graphExecutionCritthash))
        aCommandProcessor.mRite.mSentReq['Command_Election_Req'][graphExecutionCritthash] = envelope
        aCommandProcessor.mLogger.debug("Sending the %s message." % messageName)
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

class GraphCommand_Handle_Command_ExecuteGraph_ElectionFinished_Req(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        graphExecutionCritthash = self.mMessage.graphExecutionCritthash

        if    aCommandProcessor.mRite.mCritter.mCritterData.mNick \
           == aCommandProcessor.mRite.mElections[graphExecutionCritthash]['crittnick']:

            aCommandProcessor.mLogger.debug("I am the winner.")

            assert graphExecutionCritthash not in aCommandProcessor.mRite.mSentReq['Command_DetermineGraphCycle_Req'], "Not handled yet. Duplicated critthash."
            aCommandProcessor.mLogger.debug("Insert the sent request entry: [%s][%s]." % ('Command_DetermineGraphCycle_Req', graphExecutionCritthash))
            aCommandProcessor.mRite.mSentReq['Command_DetermineGraphCycle_Req'][graphExecutionCritthash] = True

            aCommandProcessor.mLogger.debug("Sending the Command_DetermineGraphCycle_Req message.")
            envelope = aCommandProcessor.mRite.mPostOffice.encode(
                'Command_DetermineGraphCycle_Req',
                {'messageName':             'Command_DetermineGraphCycle_Req',
                 'graphExecutionCritthash': graphExecutionCritthash,
                 'graphName':               self.mMessage.graphName}
            )
            aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

class GraphCommand_Handle_Command_DetermineGraphCycle_Res(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        graphExecutionCritthash = self.mMessage.graphExecutionCritthash

        if graphExecutionCritthash in aCommandProcessor.mRite.mSentReq['Command_DetermineGraphCycle_Req']:
            aCommandProcessor.mLogger.debug("Delete the sent request entry: [%s][%s]." % ('Command_DetermineGraphCycle_Req', graphExecutionCritthash))
            del aCommandProcessor.mRite.mSentReq['Command_DetermineGraphCycle_Req'][graphExecutionCritthash]

            graphCycle = self.mMessage.graphCycle
            graphName  = self.mMessage.graphName

            assert graphCycle > 0, "Invalid graphCycle value determined."

            # Create and run a session.
            if graphName not in aCommandProcessor.mRite.mSessions:
                aCommandProcessor.mRite.mSessions[graphName] = {}

            aCommandProcessor.mRite.mSessions[graphName][graphCycle] = GraphRiteSession(aCommandProcessor.mRite,
                                                                                        graphExecutionCritthash,
                                                                                        graphName,
                                                                                        graphCycle)
            aCommandProcessor.mRite.mSessions[graphName][graphCycle].setDaemon(True)
            aCommandProcessor.mRite.mSessions[graphName][graphCycle].start()

class GraphCommand_Handle_Command_Election_Res(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        critthash = self.mMessage.critthash

        # There's an active sent request.
        if critthash in aCommandProcessor.mRite.mSentReq['Command_Election_Req']:
            # Delete the sent request entry.
            del aCommandProcessor.mRite.mSentReq['Command_Election_Req'][critthash]

            # There's an active election.
            if critthash in aCommandProcessor.mRite.mElections:
                aCommandProcessor.mLogger.debug("Update the election entry: [%s]." % critthash)
                aCommandProcessor.mRite.mElections[critthash]['crittnick'] = self.mMessage.crittnick

                assert 'message' in aCommandProcessor.mRite.mElections[critthash], "There's no information about the message."
                message = aCommandProcessor.mRite.mElections[critthash]['message']

                # Handle the election topic.
                if message.messageName == 'Command_ExecuteGraph_Req':
                    command = GraphCommand_Handle_Command_ExecuteGraph_ElectionFinished_Req(message)
                    aCommandProcessor.mRite.mPostOffice.putCommand(Rites.RiteCommon.GRAPH, command)

class GraphCommand_Handle_Command_OrderWorkExecution_Res(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        workExecutionCritthash = self.mMessage.workExecutionCritthash

        messageNameSentReq = 'Command_OrderWorkExecution_Req'
        if workExecutionCritthash in aCommandProcessor.mRite.mSentReq[messageNameSentReq]:
            aCommandProcessor.mLogger.debug("Delete the sent request entry: [%s][%s]." % (messageNameSentReq, workExecutionCritthash))
            del aCommandProcessor.mRite.mSentReq[messageNameSentReq][workExecutionCritthash]

        state = GraphRiteSession.STATE_SUCCEED

        graphName  = self.mMessage.graphName
        graphCycle = self.mMessage.graphCycle
        workName   = self.mMessage.workName

        # TODO: Please, do it nicer. Consider holding exceptional cases as well.
        # REMARK: It is possible not to hit the [graphName][graphCycle] entry (e.g. due to a timeout).
        try:
            aCommandProcessor.mRite.mSessions[graphName][graphCycle].mWorkStates[workName] = state
        except KeyError, e:
            pass

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
