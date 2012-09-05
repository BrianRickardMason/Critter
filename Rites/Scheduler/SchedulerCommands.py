import os
import random

import Rites.RiteCommon

class SchedulerCommandCheckSchedule(object):
    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_STARTING:
            executor = SchedulerCommandCheckSchedule_Starting()
        elif aCommandProcessor.mRite.mState == Rites.RiteCommon.STATE_OPERABLE:
            executor = SchedulerCommandCheckSchedule_Operable()
        else:
            assert False, "Invalid state detected."

        executor.doExecute(aCommandProcessor)

class SchedulerCommandCheckSchedule_Starting(object):
    def doExecute(self, aCommandProcessor):
        aCommandProcessor.mLogger.debug("The command is not handled in this state.")

class SchedulerCommandCheckSchedule_Operable(object):
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

        executor.doExecute(aCommandProcessor)

class SchedulerCommand_Handle_Command_ExecuteGraph_Res_Starting(object):
    def doExecute(self, aCommandProcessor, aMessage):
        graphExecutionCritthash = aMessage.graphExecutionCritthash
        messageNameSentReq = 'Command_ExecuteGraph_Req'
        aCommandProcessor.mRite.deleteSentRequest(messageNameSentReq, graphExecutionCritthash)

class SchedulerCommand_Handle_Command_ExecuteGraph_Res_Operable(object):
    def doExecute(self, aCommandProcessor, aMessage):
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

        executor.doExecute(aCommandProcessor, self.mMessage)

class SchedulerCommand_Handle_Command_LoadGraphDetails_Res_Starting(object):
    def doExecute(self, aCommandProcessor, aMessage):
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
        aCommandProcessor.mRite.setState(Rites.RiteCommon.STATE_OPERABLE)

class SchedulerCommand_Handle_Command_LoadGraphDetails_Res_Operable(object):
    def doExecute(self, aCommandProcessor, aMessage):
        aCommandProcessor.mLogger.debug("The message: %s is not handled in this state." % aMessage.messageName)
