import os

import Rites.RiteCommon

from GraphRiteSession import GraphRiteSession

class GraphCommand_Auto_LoadGraphAndWork(object):
    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = GraphCommand_Auto_LoadGraphAndWork_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = GraphCommand_Auto_LoadGraphAndWork_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor)

class GraphCommand_Auto_LoadGraphAndWork_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor):
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class GraphCommand_Auto_LoadGraphAndWork_Starting(object):
    def doExecute(self, aCommand, aCommandProcessor):
        aCommandProcessor.mLogger.debug("The command: %s is handled in this state." % aCommand.__class__.__name__)

        messageName = 'Command_LoadGraphAndWork_Req'
        softTimeout = 3 # [s].
        hardTimeout = 5 # [s].
        critthash = os.urandom(32).encode('hex')
        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            messageName,
            {'messageName': messageName,
             'softTimeout': softTimeout,
             'hardTimeout': hardTimeout,
             'critthash':   critthash}
        )
        aCommandProcessor.mRite.insertSentRequest(messageName, critthash, envelope, softTimeout, hardTimeout)

class GraphCommand_Auto_LoadGraphDetails(object):
    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = GraphCommand_Auto_LoadGraphDetails_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = GraphCommand_Auto_LoadGraphDetails_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor)

class GraphCommand_Auto_LoadGraphDetails_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor):
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class GraphCommand_Auto_LoadGraphDetails_Starting(object):
    def doExecute(self, aCommand, aCommandProcessor):
        aCommandProcessor.mLogger.debug("The command: %s is handled in this state." % aCommand.__class__.__name__)

        messageName = 'Command_LoadGraphDetails_Req'
        softTimeout = 3 # [s].
        hardTimeout = 5 # [s].
        critthash = os.urandom(32).encode('hex')
        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            messageName,
            {'messageName': messageName,
             'softTimeout': softTimeout,
             'hardTimeout': hardTimeout,
             'critthash':   critthash}
        )
        aCommandProcessor.mRite.insertSentRequest(messageName, critthash, envelope, softTimeout, hardTimeout)

class GraphCommand_Auto_LoadWorkDetails(object):
    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = GraphCommand_Auto_LoadWorkDetails_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = GraphCommand_Auto_LoadWorkDetails_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor)

class GraphCommand_Auto_LoadWorkDetails_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor):
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class GraphCommand_Auto_LoadWorkDetails_Starting(object):
    def doExecute(self, aCommand, aCommandProcessor):
        aCommandProcessor.mLogger.debug("The command: %s is handled in this state." % aCommand.__class__.__name__)

        messageName = 'Command_LoadWorkDetails_Req'
        softTimeout = 3 # [s].
        hardTimeout = 5 # [s].
        critthash = os.urandom(32).encode('hex')
        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            messageName,
            {'messageName': messageName,
             'softTimeout': softTimeout,
             'hardTimeout': hardTimeout,
             'critthash':   critthash}
        )
        aCommandProcessor.mRite.insertSentRequest(messageName, critthash, envelope, softTimeout, hardTimeout)

class GraphCommand_Handle_Command_ExecuteGraph_Req(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = GraphCommand_Handle_Command_ExecuteGraph_Req_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = GraphCommand_Handle_Command_ExecuteGraph_Req_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor, self.mMessage)

class GraphCommand_Handle_Command_ExecuteGraph_Req_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        aCommandProcessor.mLogger.debug("The command: %s is handled in this state." % aCommand.__class__.__name__)

        graphExecutionCritthash = aMessage.graphExecutionCritthash

        messageName = aMessage.messageName
        aCommandProcessor.mRite.insertRecvRequest(messageName, graphExecutionCritthash, aMessage)

        assert graphExecutionCritthash not in aCommandProcessor.mRite.mElections, \
               "Not handled yet. Duplicated critthash."
        aCommandProcessor.mLogger.debug("Insert(ing) the election: [%s]." % graphExecutionCritthash)
        aCommandProcessor.mRite.mElections[graphExecutionCritthash] = {'message': aMessage}

        messageName = 'Command_Election_Req'
        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            messageName,
            {'messageName': messageName,
             'critthash':   graphExecutionCritthash,
             'crittnick':   aCommandProcessor.mRite.mCritter.mCritterData.mNick}
        )
        aCommandProcessor.mRite.insertSentRequest(messageName, graphExecutionCritthash, envelope)

class GraphCommand_Handle_Command_ExecuteGraph_Req_Starting(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class GraphCommand_Handle_Command_ExecuteGraph_ElectionFinished_Req(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = GraphCommand_Handle_Command_ExecuteGraph_ElectionFinished_Req_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = GraphCommand_Handle_Command_ExecuteGraph_ElectionFinished_Req_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor, self.mMessage)

class GraphCommand_Handle_Command_ExecuteGraph_ElectionFinished_Req_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        aCommandProcessor.mLogger.debug("The command: %s is handled in this state." % aCommand.__class__.__name__)

        graphExecutionCritthash = aMessage.graphExecutionCritthash

        if    aCommandProcessor.mRite.mCritter.mCritterData.mNick \
           == aCommandProcessor.mRite.mElections[graphExecutionCritthash]['crittnick']:

            aCommandProcessor.mLogger.debug("I am the winner.")

            messageName = 'Command_DetermineGraphCycle_Req'
            envelope = aCommandProcessor.mRite.mPostOffice.encode(
                messageName,
                {'messageName':             messageName,
                 'graphExecutionCritthash': graphExecutionCritthash,
                 'graphName':               aMessage.graphName}
            )
            aCommandProcessor.mRite.insertSentRequest(messageName, graphExecutionCritthash, envelope)

class GraphCommand_Handle_Command_ExecuteGraph_ElectionFinished_Req_Starting(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class GraphCommand_Handle_Command_DetermineGraphCycle_Res(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = GraphCommand_Handle_Command_DetermineGraphCycle_Res_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = GraphCommand_Handle_Command_DetermineGraphCycle_Res_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor, self.mMessage)

class GraphCommand_Handle_Command_DetermineGraphCycle_Res_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        aCommandProcessor.mLogger.debug("The command: %s is handled in this state." % aCommand.__class__.__name__)

        graphExecutionCritthash = aMessage.graphExecutionCritthash

        messageNameSentReq = 'Command_DetermineGraphCycle_Req'
        aCommandProcessor.mRite.deleteSentRequest(messageNameSentReq, graphExecutionCritthash)

        graphName  = aMessage.graphName
        graphCycle = aMessage.graphCycle

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

class GraphCommand_Handle_Command_DetermineGraphCycle_Res_Starting(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class GraphCommand_Handle_Command_Election_Res(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = GraphCommand_Handle_Command_Election_Res_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = GraphCommand_Handle_Command_Election_Res_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor, self.mMessage)

class GraphCommand_Handle_Command_Election_Res_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        aCommandProcessor.mLogger.debug("The command: %s is handled in this state." % aCommand.__class__.__name__)

        critthash = aMessage.critthash

        messageNameSentReq = 'Command_Election_Req'
        if critthash in aCommandProcessor.mRite.mSentReq[messageNameSentReq]:
            aCommandProcessor.mRite.deleteSentRequest(messageNameSentReq, critthash)

            if critthash in aCommandProcessor.mRite.mElections:
                aCommandProcessor.mLogger.debug("Update(ing) the election entry: [%s]." % critthash)
                aCommandProcessor.mRite.mElections[critthash]['crittnick'] = aMessage.crittnick

                assert 'message' in aCommandProcessor.mRite.mElections[critthash], "There's no information about the message."
                message = aCommandProcessor.mRite.mElections[critthash]['message']

                # Handle the election topic.
                if message.messageName == 'Command_ExecuteGraph_Req':
                    command = GraphCommand_Handle_Command_ExecuteGraph_ElectionFinished_Req(message)
                    aCommandProcessor.mRite.mPostOffice.putCommand(Rites.RiteCommon.GRAPH, command)


class GraphCommand_Handle_Command_Election_Res_Starting(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class GraphCommand_Handle_Command_LoadGraphAndWork_Res(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = GraphCommand_Handle_Command_LoadGraphAndWork_Res_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = GraphCommand_Handle_Command_LoadGraphAndWork_Res_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor, self.mMessage)

class GraphCommand_Handle_Command_LoadGraphAndWork_Res_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        # TODO: Should we always try to remove the sent request?
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class GraphCommand_Handle_Command_LoadGraphAndWork_Res_Starting(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        aCommandProcessor.mLogger.debug("The command: %s is handled in this state." % aCommand.__class__.__name__)

        messageNameSentReq = 'Command_LoadGraphAndWork_Req'
        critthash = aMessage.critthash

        if critthash in aCommandProcessor.mRite.mSentReq[messageNameSentReq]:
            # Store graphs.
            for graph in aMessage.graphs:
                aCommandProcessor.mRite.mGraphs.append(graph.graphName)

            # Store works.
            for work in aMessage.works:
                if work.graphName not in aCommandProcessor.mRite.mWorks:
                    aCommandProcessor.mRite.mWorks[work.graphName] = []

                aCommandProcessor.mRite.mWorks[work.graphName].append(work.workName)

            # Store predecessors.
            for predecessor in aMessage.workPredecessors:
                if predecessor.workName not in aCommandProcessor.mRite.mWorkPredecessors:
                    aCommandProcessor.mRite.mWorkPredecessors[predecessor.workName] = []

                aCommandProcessor.mRite.mWorkPredecessors[predecessor.workName].append(predecessor.predecessorWorkName)

        command = GraphCommand_Auto_LoadGraphDetails()
        aCommandProcessor.mRite.mPostOffice.putCommand(Rites.RiteCommon.GRAPH, command)

        aCommandProcessor.mRite.deleteSentRequest(messageNameSentReq, critthash)

class GraphCommand_Handle_Command_LoadGraphDetails_Res(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = GraphCommand_Handle_Command_LoadGraphDetails_Res_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = GraphCommand_Handle_Command_LoadGraphDetails_Res_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor, self.mMessage)

class GraphCommand_Handle_Command_LoadGraphDetails_Res_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        # TODO: Should we always try to remove the sent request?
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class GraphCommand_Handle_Command_LoadGraphDetails_Res_Starting(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        aCommandProcessor.mLogger.debug("The command: %s is handled in this state." % aCommand.__class__.__name__)

        messageNameSentReq = 'Command_LoadGraphDetails_Req'
        critthash = aMessage.critthash

        if critthash in aCommandProcessor.mRite.mSentReq[messageNameSentReq]:
            # Store graph details.
            for graphDetail in aMessage.graphDetails:
                aCommandProcessor.mRite.mGraphDetails[graphDetail.graphName] = {
                    'graphName':   graphDetail.graphName,
                    'softTimeout': graphDetail.softTimeout,
                    'hardTimeout': graphDetail.hardTimeout
                }

        command = GraphCommand_Auto_LoadWorkDetails()
        aCommandProcessor.mRite.mPostOffice.putCommand(Rites.RiteCommon.GRAPH, command)

        aCommandProcessor.mRite.deleteSentRequest(messageNameSentReq, critthash)

class GraphCommand_Handle_Command_LoadWorkDetails_Res(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = GraphCommand_Handle_Command_LoadWorkDetails_Res_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = GraphCommand_Handle_Command_LoadWorkDetails_Res_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor, self.mMessage)

class GraphCommand_Handle_Command_LoadWorkDetails_Res_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        # TODO: Should we always try to remove the sent request?
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class GraphCommand_Handle_Command_LoadWorkDetails_Res_Starting(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        aCommandProcessor.mLogger.debug("The command: %s is handled in this state." % aCommand.__class__.__name__)

        messageNameSentReq = 'Command_LoadWorkDetails_Req'
        critthash = aMessage.critthash

        if critthash in aCommandProcessor.mRite.mSentReq[messageNameSentReq]:
            # Store work details.
            for workDetail in aMessage.workDetails:
                aCommandProcessor.mRite.mWorkDetails[workDetail.workName] = {
                    'workName':    workDetail.workName,
                    'softTimeout': workDetail.softTimeout,
                    'hardTimeout': workDetail.hardTimeout,
                    'dummy':       workDetail.dummy
                }

        aCommandProcessor.mRite.setState(Rites.RiteCommon.STATE_OPERABLE)

        aCommandProcessor.mRite.deleteSentRequest(messageNameSentReq, critthash)

class GraphCommand_Handle_Command_OrderWorkExecution_Res(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = GraphCommand_Handle_Command_OrderWorkExecution_Res_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = GraphCommand_Handle_Command_OrderWorkExecution_Res_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor, self.mMessage)

class GraphCommand_Handle_Command_OrderWorkExecution_Res_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        aCommandProcessor.mLogger.debug("The command: %s is handled in this state." % aCommand.__class__.__name__)

        workExecutionCritthash = aMessage.workExecutionCritthash

        messageNameSentReq = 'Command_OrderWorkExecution_Req'
        aCommandProcessor.mRite.deleteSentRequest(messageNameSentReq, workExecutionCritthash)

        state = GraphRiteSession.STATE_SUCCEED

        graphName  = aMessage.graphName
        graphCycle = aMessage.graphCycle
        workName   = aMessage.workName

        # TODO: Please, do it nicer. Consider holding exceptional cases as well.
        # REMARK: It is possible not to hit the [graphName][graphCycle] entry (e.g. due to a timeout).
        try:
            aCommandProcessor.mRite.mSessions[graphName][graphCycle].mWorkStates[workName] = state
        except KeyError, e:
            pass

class GraphCommand_Handle_Command_OrderWorkExecution_Res_Starting(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)
