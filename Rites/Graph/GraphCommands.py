import os

import Rites.RiteCommon

from GraphRiteSession import GraphRiteSession

class GraphCommand_Handle_Command_Req_ExecuteGraph(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        critthash = self.mMessage.critthash

        assert self.mMessage.messageName in aCommandProcessor.mRite.mRecvReq, "Missing key in the dictionary of received requests."
        assert critthash not in aCommandProcessor.mRite.mRecvReq[self.mMessage.messageName], "Not handled yet. Duplicated critthash."
        aCommandProcessor.mLogger.debug("Insert the received request entry: [%s][%s]." % (self.mMessage.messageName, critthash))
        aCommandProcessor.mRite.mRecvReq[self.mMessage.messageName][critthash] = True

        assert critthash not in aCommandProcessor.mRite.mElections, "Not handled yet. Duplicated critthash."
        aCommandProcessor.mLogger.debug("Insert the election entry: [%s]." % critthash)
        aCommandProcessor.mRite.mElections[critthash] = {'message': self.mMessage}

        assert 'Command_Req_Election' in aCommandProcessor.mRite.mSentReq, "Missing key in the dictionary of sent requests."
        assert critthash not in aCommandProcessor.mRite.mSentReq['Command_Req_Election'], "Not handled yet. Duplicated critthash."
        aCommandProcessor.mLogger.debug("Insert the sent request entry: [%s][%s]." % ('Command_Req_Election', critthash))
        aCommandProcessor.mRite.mSentReq['Command_Req_Election'][critthash] = True

        aCommandProcessor.mLogger.debug("Sending the Command_Req_ExecuteGraph message.")
        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            'Command_Req_Election',
            {'messageName': 'Command_Req_Election',
             'critthash':   critthash,
             'crittnick':   aCommandProcessor.mRite.mCritter.mCritterData.mNick}
        )
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

class GraphCommand_Handle_Command_Req_ExecuteGraph_ElectionFinished(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if    aCommandProcessor.mRite.mCritter.mCritterData.mNick \
           == aCommandProcessor.mRite.mElections[self.mMessage.critthash]['crittnick']:

            aCommandProcessor.mLogger.debug("I am the winner.")

            critthash = os.urandom(32).encode('hex')

            assert 'Command_Req_DetermineGraphCycle' in aCommandProcessor.mRite.mSentReq, "Missing key in the dictionary of sent requests."
            assert critthash not in aCommandProcessor.mRite.mSentReq['Command_Req_DetermineGraphCycle'], "Not handled yet. Duplicated critthash."
            aCommandProcessor.mLogger.debug("Insert the sent request entry: [%s][%s]." % ('Command_Req_DetermineGraphCycle', critthash))
            aCommandProcessor.mRite.mSentReq['Command_Req_DetermineGraphCycle'][critthash] = True

            aCommandProcessor.mLogger.debug("Sending the Command_Req_DetermineGraphCycle message.")
            envelope = aCommandProcessor.mRite.mPostOffice.encode(
                'Command_Req_DetermineGraphCycle',
                {'messageName': 'Command_Req_DetermineGraphCycle',
                 'critthash':   critthash,
                 'graphName':   self.mMessage.graphName}
            )
            aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

class GraphCommand_Handle_Command_Res_DetermineGraphCycle(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        assert 'Command_Req_DetermineGraphCycle' in aCommandProcessor.mRite.mSentReq, "Missing key in the dictionary of sent requests."

        critthash = self.mMessage.critthash

        if critthash in aCommandProcessor.mRite.mSentReq['Command_Req_DetermineGraphCycle']:
            aCommandProcessor.mLogger.debug("Delete the sent request entry: [%s][%s]." % ('Command_Req_DetermineGraphCycle', critthash))
            del aCommandProcessor.mRite.mSentReq['Command_Req_DetermineGraphCycle'][critthash]

            graphCycle     = self.mMessage.graphCycle
            graphName = self.mMessage.graphName

            assert graphCycle > 0, "Invalid graph cycle value determined."

            # Create and run a session.
            if graphName not in aCommandProcessor.mRite.mSessions:
                aCommandProcessor.mRite.mSessions[graphName] = {}

            aCommandProcessor.mRite.mSessions[graphName][graphCycle] = GraphRiteSession(aCommandProcessor.mRite,
                                                                                        graphName,
                                                                                        graphCycle)
            aCommandProcessor.mRite.mSessions[graphName][graphCycle].setDaemon(True)
            aCommandProcessor.mRite.mSessions[graphName][graphCycle].start()

class GraphCommand_Handle_Command_Res_Election(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        critthash = self.mMessage.critthash

        # There's an active sent request.
        if critthash in aCommandProcessor.mRite.mSentReq['Command_Req_Election']:
            # Delete the sent request entry.
            del aCommandProcessor.mRite.mSentReq['Command_Req_Election'][critthash]

            # There's an active election.
            if critthash in aCommandProcessor.mRite.mElections:
                aCommandProcessor.mLogger.debug("Extending the election entry: [%s]." % critthash)
                aCommandProcessor.mRite.mElections[critthash]['crittnick'] = self.mMessage.crittnick

                assert 'message' in aCommandProcessor.mRite.mElections[critthash], "There's no information about the message."
                message = aCommandProcessor.mRite.mElections[critthash]['message']

                # Handle the election topic.
                if message.messageName == 'Command_Req_ExecuteGraph':
                    command = GraphCommand_Handle_Command_Req_ExecuteGraph_ElectionFinished(message)
                    aCommandProcessor.mRite.mPostOffice.putCommand(Rites.RiteCommon.GRAPH, command)

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
