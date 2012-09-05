import os
import random

import Rites.RiteCommon

class SchedulerCommand_Auto_CheckSchedule(object):
    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = SchedulerCommand_Auto_CheckSchedule_Starting()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = SchedulerCommand_Auto_CheckSchedule_Operable()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(aCommandProcessor)

class SchedulerCommand_Auto_CheckSchedule_Operable(object):
    def doExecute(self, aCommandProcessor):
        # FIXME: This simulates the need of graph execution.
        if random.randint(1, 100) > 50:
            aCommandProcessor.mLogger.info("New graph execution needed.")

            graphNames = ['GraphName1', 'GraphName2', 'GraphName3', 'GraphName4']

            graphExecutionCritthash = os.urandom(32).encode('hex')
            messageName = 'Command_ExecuteGraph_Req'

            envelope = aCommandProcessor.mRite.mPostOffice.encode(
                messageName,
                {'messageName':             messageName,
                 'graphExecutionCritthash': graphExecutionCritthash,
                 'graphName':               random.choice(graphNames)}
            )
            aCommandProcessor.mRite.insertSentRequest(messageName, graphExecutionCritthash, envelope)

class SchedulerCommand_Auto_CheckSchedule_Starting(object):
    def doExecute(self, aCommandProcessor):
        aCommandProcessor.mLogger.debug("The command is not handled in this state.")

class SchedulerCommand_Auto_LoadGraphDetails(object):
    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = SchedulerCommand_Auto_LoadGraphDetails_Starting()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = SchedulerCommand_Auto_LoadGraphDetails_Operable()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor)

class SchedulerCommand_Auto_LoadGraphDetails_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor):
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class SchedulerCommand_Auto_LoadGraphDetails_Starting(object):
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

class SchedulerCommand_Auto_LoadWorkDetails(object):
    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = SchedulerCommand_Auto_LoadWorkDetails_Starting()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = SchedulerCommand_Auto_LoadWorkDetails_Operable()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor)

class SchedulerCommand_Auto_LoadWorkDetails_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor):
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class SchedulerCommand_Auto_LoadWorkDetails_Starting(object):
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

class SchedulerCommand_Handle_Command_ExecuteGraph_Res(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = SchedulerCommand_Handle_Command_ExecuteGraph_Res_Starting()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = SchedulerCommand_Handle_Command_ExecuteGraph_Res_Operable()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor, self.mMessage)

class SchedulerCommand_Handle_Command_ExecuteGraph_Res_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        aCommandProcessor.mLogger.debug("The command: %s is handled in this state." % aCommand.__class__.__name__)

        graphExecutionCritthash = aMessage.graphExecutionCritthash
        messageNameSentReq = 'Command_ExecuteGraph_Req'
        aCommandProcessor.mRite.deleteSentRequest(messageNameSentReq, graphExecutionCritthash)

class SchedulerCommand_Handle_Command_ExecuteGraph_Res_Starting(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        aCommandProcessor.mLogger.debug("The command: %s is handled in this state." % aCommand.__class__.__name__)

        graphExecutionCritthash = aMessage.graphExecutionCritthash
        messageNameSentReq = 'Command_ExecuteGraph_Req'
        aCommandProcessor.mRite.deleteSentRequest(messageNameSentReq, graphExecutionCritthash)

class SchedulerCommand_Handle_Command_LoadGraphDetails_Res(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = SchedulerCommand_Handle_Command_LoadGraphDetails_Res_Starting()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = SchedulerCommand_Handle_Command_LoadGraphDetails_Res_Operable()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor, self.mMessage)

class SchedulerCommand_Handle_Command_LoadGraphDetails_Res_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        # TODO: Should we always try to remove the sent request?
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class SchedulerCommand_Handle_Command_LoadGraphDetails_Res_Starting(object):
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

        aCommandProcessor.mRite.deleteSentRequest(messageNameSentReq, critthash)

        command = SchedulerCommand_Auto_LoadWorkDetails()
        aCommandProcessor.mRite.mPostOffice.putCommand(Rites.RiteCommon.SCHEDULER, command)

class SchedulerCommand_Handle_Command_LoadWorkDetails_Res(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = SchedulerCommand_Handle_Command_LoadWorkDetails_Res_Starting()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = SchedulerCommand_Handle_Command_LoadWorkDetails_Res_Operable()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(self, aCommandProcessor, self.mMessage)

class SchedulerCommand_Handle_Command_LoadWorkDetails_Res_Operable(object):
    def doExecute(self, aCommand, aCommandProcessor, aMessage):
        # TODO: Should we always try to remove the sent request?
        aCommandProcessor.mLogger.debug("The command: %s is not handled in this state." % aCommand.__class__.__name__)

class SchedulerCommand_Handle_Command_LoadWorkDetails_Res_Starting(object):
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

        aCommandProcessor.mRite.deleteSentRequest(messageNameSentReq, critthash)
        aCommandProcessor.mRite.setState(Rites.RiteCommon.STATE_OPERABLE)
        print "ASD"
