import os

import Rites.RiteCommon

from WorkRiteSession import WorkRiteSession

class WorkCommand_Auto_LoadGraphAndWork(object):
    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = WorkCommand_Auto_LoadGraphAndWork_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = WorkCommand_Auto_LoadGraphAndWork_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor)

class WorkCommand_Auto_LoadGraphAndWork_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor):
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class WorkCommand_Auto_LoadGraphAndWork_Starting(object):
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

class WorkCommand_Auto_LoadGraphDetails(object):
    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = WorkCommand_Auto_LoadGraphDetails_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = WorkCommand_Auto_LoadGraphDetails_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor)

class WorkCommand_Auto_LoadGraphDetails_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor):
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class WorkCommand_Auto_LoadGraphDetails_Starting(object):
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

class WorkCommand_Auto_LoadWorkDetails(object):
    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = WorkCommand_Auto_LoadWorkDetails_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = WorkCommand_Auto_LoadWorkDetails_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor)

class WorkCommand_Auto_LoadWorkDetails_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor):
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class WorkCommand_Auto_LoadWorkDetails_Starting(object):
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

class WorkCommand_Handle_Command_DetermineWorkCycle_Res(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = WorkCommand_Handle_Command_DetermineWorkCycle_Res_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = WorkCommand_Handle_Command_DetermineWorkCycle_Res_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor, self.mMessage)

class WorkCommand_Handle_Command_DetermineWorkCycle_Res_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        aCommandProcessor.mLogger.debug("The command: %s is handled in this state." % aCommand.__class__.__name__)

        workExecutionCritthash = aMessage.workExecutionCritthash

        messageNameSentReq = 'Command_DetermineWorkCycle_Req'
        if workExecutionCritthash in aCommandProcessor.mRite.mSentReq[messageNameSentReq]:
            aCommandProcessor.mRite.deleteSentRequest(messageNameSentReq, workExecutionCritthash)

            graphCycle = aMessage.graphCycle
            workCycle  = aMessage.workCycle
            workName   = aMessage.workName

            assert graphCycle > 0, "Invalid graphCycle value determined."
            assert workCycle  > 0, "Invalid workCycle value determined."

            # Create and run a session.
            if workName not in aCommandProcessor.mRite.mSessions:
                aCommandProcessor.mRite.mSessions[workName] = {}

            aCommandProcessor.mRite.mSessions[workName][workCycle] = WorkRiteSession(aCommandProcessor.mRite,
                                                                                     aMessage.graphExecutionCritthash,
                                                                                     aMessage.graphName,
                                                                                     graphCycle,
                                                                                     workExecutionCritthash,
                                                                                     workName,
                                                                                     workCycle)
            aCommandProcessor.mRite.mSessions[workName][workCycle].setDaemon(True)
            aCommandProcessor.mRite.mSessions[workName][workCycle].start()

class WorkCommand_Handle_Command_DetermineWorkCycle_Res_Starting(object):
    def doExecute(self, aCommand, aCommandProcessor):
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class WorkCommand_Handle_Command_ExecuteWork_Req(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = WorkCommand_Handle_Command_ExecuteWork_Req_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = WorkCommand_Handle_Command_ExecuteWork_Req_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor, self.mMessage)

class WorkCommand_Handle_Command_ExecuteWork_Req_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        aCommandProcessor.mLogger.debug("The command: %s is handled in this state." % aCommand.__class__.__name__)

        if aCommandProcessor.mRite.mCritter.mCrittnick == aMessage.receiverCrittnick:
            aCommandProcessor.mLogger.debug("I have been selected.")

            workExecutionCritthash = aMessage.workExecutionCritthash

            messageName = aMessage.messageName
            aCommandProcessor.mRite.insertRecvRequest(messageName, workExecutionCritthash, aMessage)

            messageName = 'Command_DetermineWorkCycle_Req'
            envelope = aCommandProcessor.mRite.mPostOffice.encode(
                messageName,
                {'messageName':             messageName,
                 'graphExecutionCritthash': aMessage.graphExecutionCritthash,
                 'graphName':               aMessage.graphName,
                 'graphCycle':              aMessage.graphCycle,
                 'workExecutionCritthash':  aMessage.workExecutionCritthash,
                 'workName':                aMessage.workName}
            )
            aCommandProcessor.mRite.insertSentRequest(messageName, workExecutionCritthash, envelope)

class WorkCommand_Handle_Command_ExecuteWork_Req_Starting(object):
    def doExecute(self, aCommand, aCommandProcessor):
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class WorkCommand_Handle_Command_LoadGraphAndWork_Res(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = WorkCommand_Handle_Command_LoadGraphAndWork_Res_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = WorkCommand_Handle_Command_LoadGraphAndWork_Res_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor, self.mMessage)

class WorkCommand_Handle_Command_LoadGraphAndWork_Res_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        # TODO: Should we always try to remove the sent request?
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class WorkCommand_Handle_Command_LoadGraphAndWork_Res_Starting(object):
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

        command = WorkCommand_Auto_LoadGraphDetails()
        aCommandProcessor.mRite.mPostOffice.putCommand(Rites.RiteCommon.WORK, command)

        aCommandProcessor.mRite.deleteSentRequest(messageNameSentReq, critthash)

class WorkCommand_Handle_Command_LoadGraphDetails_Res(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = WorkCommand_Handle_Command_LoadGraphDetails_Res_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = WorkCommand_Handle_Command_LoadGraphDetails_Res_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor, self.mMessage)

class WorkCommand_Handle_Command_LoadGraphDetails_Res_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        # TODO: Should we always try to remove the sent request?
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class WorkCommand_Handle_Command_LoadGraphDetails_Res_Starting(object):
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

        command = WorkCommand_Auto_LoadWorkDetails()
        aCommandProcessor.mRite.mPostOffice.putCommand(Rites.RiteCommon.WORK, command)

        aCommandProcessor.mRite.deleteSentRequest(messageNameSentReq, critthash)

class WorkCommand_Handle_Command_LoadWorkDetails_Res(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = WorkCommand_Handle_Command_LoadWorkDetails_Res_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = WorkCommand_Handle_Command_LoadWorkDetails_Res_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor, self.mMessage)

class WorkCommand_Handle_Command_LoadWorkDetails_Res_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        # TODO: Should we always try to remove the sent request?
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class WorkCommand_Handle_Command_LoadWorkDetails_Res_Starting(object):
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
