import os

from random import choice

import Rites.RiteCommon

class BalanceCommand_Auto_LoadGraphAndWork(object):
    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = BalanceCommand_Auto_LoadGraphAndWork_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = BalanceCommand_Auto_LoadGraphAndWork_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor)

class BalanceCommand_Auto_LoadGraphAndWork_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor):
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class BalanceCommand_Auto_LoadGraphAndWork_Starting(object):
    def doExecute(self, aCommand, aCommandProcessor):
        aCommandProcessor.mLogger.debug("The command: %s is handled in this state." % aCommand.__class__.__name__)

        messageName = 'Command_LoadGraphAndWork_Req'
        softTimeout = 3 # [s].
        hardTimeout = 5 # [s].
        critthash = os.urandom(32).encode('hex')
        message = aCommandProcessor.mRite.mPostOffice.encode({
            'messageName': messageName,
            'softTimeout': softTimeout,
            'hardTimeout': hardTimeout,
            'critthash':   critthash
        })
        aCommandProcessor.mRite.insertSentRequest(messageName, critthash, message, softTimeout, hardTimeout)

class BalanceCommand_Auto_LoadGraphDetails(object):
    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = BalanceCommand_Auto_LoadGraphDetails_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = BalanceCommand_Auto_LoadGraphDetails_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor)

class BalanceCommand_Auto_LoadGraphDetails_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor):
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class BalanceCommand_Auto_LoadGraphDetails_Starting(object):
    def doExecute(self, aCommand, aCommandProcessor):
        aCommandProcessor.mLogger.debug("The command: %s is handled in this state." % aCommand.__class__.__name__)

        messageName = 'Command_LoadGraphDetails_Req'
        softTimeout = 3 # [s].
        hardTimeout = 5 # [s].
        critthash = os.urandom(32).encode('hex')
        message = aCommandProcessor.mRite.mPostOffice.encode({
            'messageName': messageName,
            'softTimeout': softTimeout,
            'hardTimeout': hardTimeout,
            'critthash':   critthash
        })
        aCommandProcessor.mRite.insertSentRequest(messageName, critthash, message, softTimeout, hardTimeout)

class BalanceCommand_Auto_LoadWorkDetails(object):
    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = BalanceCommand_Auto_LoadWorkDetails_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = BalanceCommand_Auto_LoadWorkDetails_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor)

class BalanceCommand_Auto_LoadWorkDetails_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor):
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class BalanceCommand_Auto_LoadWorkDetails_Starting(object):
    def doExecute(self, aCommand, aCommandProcessor):
        aCommandProcessor.mLogger.debug("The command: %s is handled in this state." % aCommand.__class__.__name__)

        messageName = 'Command_LoadWorkDetails_Req'
        softTimeout = 3 # [s].
        hardTimeout = 5 # [s].
        critthash = os.urandom(32).encode('hex')
        message = aCommandProcessor.mRite.mPostOffice.encode({
            'messageName': messageName,
            'softTimeout': softTimeout,
            'hardTimeout': hardTimeout,
            'critthash':   critthash
        })
        aCommandProcessor.mRite.insertSentRequest(messageName, critthash, message, softTimeout, hardTimeout)

class BalanceCommand_Handle_Command_Election_Res(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = BalanceCommand_Handle_Command_Election_Res_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = BalanceCommand_Handle_Command_Election_Res_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor, self.mMessage)

class BalanceCommand_Handle_Command_Election_Res_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        critthash = aMessage.critthash

        aCommandProcessor.mLogger.debug("The command: %s is handled in this state." % aCommand.__class__.__name__)

        messageNameSentReq = 'Command_Election_Req'
        if critthash in aCommandProcessor.mRite.mSentReq[messageNameSentReq]:
            aCommandProcessor.mRite.deleteSentRequest(messageNameSentReq, critthash)

            if critthash in aCommandProcessor.mRite.mElections:
                aCommandProcessor.mLogger.debug("Update(ing) the election entry: [%s]." % critthash)
                aCommandProcessor.mRite.mElections[critthash]['crittnick'] = aMessage.crittnick

                assert 'message' in aCommandProcessor.mRite.mElections[critthash], "There's no information about the message."
                message = aCommandProcessor.mRite.mElections[critthash]['message']

                # Handle the election topic.
                if message.messageName == 'Command_OrderWorkExecution_Req':
                    command = BalanceCommand_Handle_Command_OrderWorkExecution_ElectionFinished_Req(message)
                    aCommandProcessor.mRite.mPostOffice.putCommand(Rites.RiteCommon.BALANCE, command)

class BalanceCommand_Handle_Command_Election_Res_Starting(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class BalanceCommand_Handle_Command_ExecuteWork_Res(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = BalanceCommand_Handle_Command_ExecuteWork_Res_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = BalanceCommand_Handle_Command_ExecuteWork_Res_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor, self.mMessage)

class BalanceCommand_Handle_Command_ExecuteWork_Res_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        aCommandProcessor.mLogger.debug("The command: %s is handled in this state." % aCommand.__class__.__name__)

        workExecutionCritthash = aMessage.workExecutionCritthash

        messageNameSentReq = 'Command_ExecuteWork_Req'
        if workExecutionCritthash in aCommandProcessor.mRite.mSentReq[messageNameSentReq]:
            aCommandProcessor.mRite.deleteSentRequest(messageNameSentReq, workExecutionCritthash)

        messageNameRecvReq = 'Command_OrderWorkExecution_Req'
        messageNameRecvRes = 'Command_OrderWorkExecution_Res'
        message = aCommandProcessor.mRite.mPostOffice.encode({
            'messageName':             messageNameRecvRes,
            'graphExecutionCritthash': aMessage.graphExecutionCritthash,
            'graphName':               aMessage.graphName,
            'graphCycle':              aMessage.graphCycle,
            'workExecutionCritthash':  aMessage.workExecutionCritthash,
            'workName':                aMessage.workName
        })
        aCommandProcessor.mRite.deleteRecvRequest(messageNameRecvReq, workExecutionCritthash)
        aCommandProcessor.mLogger.debug("Sending the %s message." % messageNameRecvRes)
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(message)

class BalanceCommand_Handle_Command_ExecuteWork_Res_Starting(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class BalanceCommand_Handle_Command_LoadGraphAndWork_Res(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = BalanceCommand_Handle_Command_LoadGraphAndWork_Res_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = BalanceCommand_Handle_Command_LoadGraphAndWork_Res_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor, self.mMessage)

class BalanceCommand_Handle_Command_LoadGraphAndWork_Res_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        # TODO: Should we always try to remove the sent request?
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class BalanceCommand_Handle_Command_LoadGraphAndWork_Res_Starting(object):
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

        command = BalanceCommand_Auto_LoadGraphDetails()
        aCommandProcessor.mRite.mPostOffice.putCommand(Rites.RiteCommon.BALANCE, command)

        aCommandProcessor.mRite.deleteSentRequest(messageNameSentReq, critthash)

class BalanceCommand_Handle_Command_LoadGraphDetails_Res(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = BalanceCommand_Handle_Command_LoadGraphDetails_Res_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = BalanceCommand_Handle_Command_LoadGraphDetails_Res_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor, self.mMessage)

class BalanceCommand_Handle_Command_LoadGraphDetails_Res_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        # TODO: Should we always try to remove the sent request?
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class BalanceCommand_Handle_Command_LoadGraphDetails_Res_Starting(object):
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

        command = BalanceCommand_Auto_LoadWorkDetails()
        aCommandProcessor.mRite.mPostOffice.putCommand(Rites.RiteCommon.BALANCE, command)

        aCommandProcessor.mRite.deleteSentRequest(messageNameSentReq, critthash)

class BalanceCommand_Handle_Command_LoadWorkDetails_Res(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = BalanceCommand_Handle_Command_LoadWorkDetails_Res_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = BalanceCommand_Handle_Command_LoadWorkDetails_Res_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor, self.mMessage)

class BalanceCommand_Handle_Command_LoadWorkDetails_Res_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        # TODO: Should we always try to remove the sent request?
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class BalanceCommand_Handle_Command_LoadWorkDetails_Res_Starting(object):
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

class BalanceCommand_Handle_Command_OrderWorkExecution_ElectionFinished_Req(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = BalanceCommand_Handle_Command_OrderWorkExecution_ElectionFinished_Req_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = BalanceCommand_Handle_Command_OrderWorkExecution_ElectionFinished_Req_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor, self.mMessage)

class BalanceCommand_Handle_Command_OrderWorkExecution_ElectionFinished_Req_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        aCommandProcessor.mLogger.debug("The command: %s is handled in this state." % aCommand.__class__.__name__)

        workExecutionCritthash = aMessage.workExecutionCritthash

        if    aCommandProcessor.mRite.mCritter.mCrittnick \
           == aCommandProcessor.mRite.mElections[workExecutionCritthash]['crittnick']:

            aCommandProcessor.mLogger.debug("I am the winner.")

            # FIXME: Synchronous, argh!
            knownCritters = aCommandProcessor.mRite.mCritter.mRites[Rites.RiteCommon.REGISTRY].getKnownCritters()

            # Filter workers.
            availableWorkers = []
            for key in knownCritters[2]:
                for rites in knownCritters[2][key]:
                    if Rites.RiteCommon.WORK in rites:
                        availableWorkers.append(key)

            # Balance the load.
            # FIXME: What happens when there are not any workers?
            receiverCrittnick = choice(availableWorkers)

            messageName = 'Command_ExecuteWork_Req'
            message = aCommandProcessor.mRite.mPostOffice.encode({
                'messageName':             messageName,
                'receiverCrittnick':       receiverCrittnick,
                'graphExecutionCritthash': aMessage.graphExecutionCritthash,
                'graphName':               aMessage.graphName,
                'graphCycle':              aMessage.graphCycle,
                'workExecutionCritthash':  aMessage.workExecutionCritthash,
                'workName':                aMessage.workName
            })
            aCommandProcessor.mRite.insertSentRequest(messageName, workExecutionCritthash, message)

        if workExecutionCritthash in aCommandProcessor.mRite.mElections:
            aCommandProcessor.mLogger.debug("Delete(ing) the election: [%s]." % (workExecutionCritthash))
            del aCommandProcessor.mRite.mElections[workExecutionCritthash]

class BalanceCommand_Handle_Command_OrderWorkExecution_ElectionFinished_Req_Starting(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class BalanceCommand_Handle_Command_OrderWorkExecution_Req(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = BalanceCommand_Handle_Command_OrderWorkExecution_Req_Operable()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = BalanceCommand_Handle_Command_OrderWorkExecution_Req_Starting()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor, self.mMessage)

class BalanceCommand_Handle_Command_OrderWorkExecution_Req_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        aCommandProcessor.mLogger.debug("The command: %s is handled in this state." % aCommand.__class__.__name__)

        workExecutionCritthash = aMessage.workExecutionCritthash

        messageName = aMessage.messageName
        aCommandProcessor.mRite.insertRecvRequest(messageName, workExecutionCritthash, aMessage)

        assert workExecutionCritthash not in aCommandProcessor.mRite.mElections, "Not handled yet. Duplicated critthash."
        aCommandProcessor.mLogger.debug("Insert(ing) the election: [%s]." % workExecutionCritthash)
        aCommandProcessor.mRite.mElections[workExecutionCritthash] = {'message': aMessage}

        messageName = 'Command_Election_Req'
        message = aCommandProcessor.mRite.mPostOffice.encode({
            'messageName': messageName,
            'critthash':   workExecutionCritthash,
            'crittnick':   aCommandProcessor.mRite.mCritter.mCrittnick
        })
        aCommandProcessor.mRite.insertSentRequest(messageName, workExecutionCritthash, message)

class BalanceCommand_Handle_Command_OrderWorkExecution_Req_Starting(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)
