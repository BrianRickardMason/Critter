import os
import random

class SchedulerCommandCheckSchedule(object):
    def execute(self, aCommandProcessor):
        # FIXME: This simulates the need of graph execution.
        if random.randint(1, 100) > 50:
            aCommandProcessor.mLogger.info("New graph execution needed.")

            graphNames = ['GraphName1', 'GraphName2', 'GraphName3', 'GraphName4']

            graphExecutionCritthash = os.urandom(32).encode('hex')

            assert graphExecutionCritthash not in aCommandProcessor.mRite.mSentReq['Command_ExecuteGraph_Req'], "Not handled yet. Duplicated critthash."

            aCommandProcessor.mLogger.debug("Insert the sent message entry: [%s][%s]." % ('Command_ExecuteGraph_Req', graphExecutionCritthash))
            aCommandProcessor.mRite.mSentReq['Command_ExecuteGraph_Req'][graphExecutionCritthash] = {'graphExecutionCritthash': graphExecutionCritthash}

            aCommandProcessor.mLogger.debug("Sending the Command_ExecuteGraph_Req message.")
            envelope = aCommandProcessor.mRite.mPostOffice.encode(
                'Command_ExecuteGraph_Req',
                {'messageName':             'Command_ExecuteGraph_Req',
                 'graphExecutionCritthash': graphExecutionCritthash,
                 'graphName':               random.choice(graphNames)}
            )
            aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

class SchedulerCommand_Handle_Command_ExecuteGraph_Res(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        graphExecutionCritthash = self.mMessage.graphExecutionCritthash

        messageNameSentReq = 'Command_ExecuteGraph_Req'
        if graphExecutionCritthash in aCommandProcessor.mRite.mSentReq[messageNameSentReq]:
            aCommandProcessor.mLogger.debug("Delete(ing) the sent request: [%s][%s]." % (messageNameSentReq, graphExecutionCritthash))
            del aCommandProcessor.mRite.mSentReq[messageNameSentReq][graphExecutionCritthash]
