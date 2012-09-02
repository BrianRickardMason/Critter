from random import choice

import Rites.RiteCommon

class BalanceCommand_Handle_Command_OrderWorkExecution_Req(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        workExecutionCritthash = self.mMessage.workExecutionCritthash

        messageName = self.mMessage.messageName
        assert workExecutionCritthash not in aCommandProcessor.mRite.mRecvReq[messageName], "Not handled yet. Duplicated critthash."
        aCommandProcessor.mLogger.debug("Insert the received request entry: [%s][%s]." % (messageName, workExecutionCritthash))
        aCommandProcessor.mRite.mRecvReq[messageName][workExecutionCritthash] = self.mMessage

        assert workExecutionCritthash not in aCommandProcessor.mRite.mElections, "Not handled yet. Duplicated critthash."
        aCommandProcessor.mLogger.debug("Insert the election entry: [%s]." % workExecutionCritthash)
        aCommandProcessor.mRite.mElections[workExecutionCritthash] = {'message': self.mMessage}

        messageName = 'Command_Election_Req'
        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            messageName,
            {'messageName': messageName,
             'critthash':   workExecutionCritthash,
             'crittnick':   aCommandProcessor.mRite.mCritter.mCritterData.mNick}
        )
        assert workExecutionCritthash not in aCommandProcessor.mRite.mSentReq[messageName], "Not handled yet. Duplicated critthash."
        aCommandProcessor.mLogger.debug("Insert the sent request entry: [%s][%s]." % (messageName, workExecutionCritthash))
        aCommandProcessor.mRite.mSentReq[messageName][workExecutionCritthash] = envelope
        aCommandProcessor.mLogger.debug("Sending the %s message." % messageName)
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

class BalanceCommand_Handle_Command_OrderWorkExecution_ElectionFinished_Req(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        workExecutionCritthash = self.mMessage.workExecutionCritthash

        if    aCommandProcessor.mRite.mCritter.mCritterData.mNick \
           == aCommandProcessor.mRite.mElections[workExecutionCritthash]['crittnick']:

            aCommandProcessor.mLogger.debug("I am the winner.")

            knownCritters = aCommandProcessor.mRite.mCritter.mRites[Rites.RiteCommon.REGISTRY].getKnownCritters()

            # Filter workers.
            availableWorkers = []
            for critterData in knownCritters.values():
                if critterData.mType == 'Worker':
                    availableWorkers.append(critterData.mNick)

            # Balance the load.
            # FIXME: What happens when there are not any workers?
            receiverCrittnick = choice(availableWorkers)

            messageName = 'Command_ExecuteWork_Req'
            envelope = aCommandProcessor.mRite.mPostOffice.encode(
                messageName,
                {'messageName':             messageName,
                 'receiverCrittnick':       receiverCrittnick,
                 'graphExecutionCritthash': self.mMessage.graphExecutionCritthash,
                 'graphName':               self.mMessage.graphName,
                 'graphCycle':              self.mMessage.graphCycle,
                 'workExecutionCritthash':  self.mMessage.workExecutionCritthash,
                 'workName':                self.mMessage.workName}
            )
            assert workExecutionCritthash not in aCommandProcessor.mRite.mSentReq[messageName], "Not handled yet. Duplicated critthash."
            aCommandProcessor.mLogger.debug("Insert the sent request entry: [%s][%s]." % (messageName, workExecutionCritthash))
            aCommandProcessor.mRite.mSentReq[messageName][workExecutionCritthash] = envelope
            aCommandProcessor.mLogger.debug("Sending the %s message." % messageName)
            aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

class BalanceCommand_Handle_Command_Election_Res(object):
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
                if message.messageName == 'Command_OrderWorkExecution_Req':
                    command = BalanceCommand_Handle_Command_OrderWorkExecution_ElectionFinished_Req(message)
                    aCommandProcessor.mRite.mPostOffice.putCommand(Rites.RiteCommon.BALANCE, command)

class BalanceCommand_Handle_Command_ExecuteWork_Res(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        workExecutionCritthash = self.mMessage.workExecutionCritthash

        messageNameSentReq = 'Command_ExecuteWork_Req'
        if workExecutionCritthash in aCommandProcessor.mRite.mSentReq[messageNameSentReq]:
            aCommandProcessor.mLogger.debug("Delete the sent request entry: [%s][%s]." % (messageNameSentReq, workExecutionCritthash))
            del aCommandProcessor.mRite.mSentReq[messageNameSentReq][workExecutionCritthash]

        messageNameRecvReq = 'Command_OrderWorkExecution_Req'
        messageNameRecvRes = 'Command_OrderWorkExecution_Res'
        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            messageNameRecvRes,
            {'messageName':             messageNameRecvRes,
             'graphExecutionCritthash': self.mMessage.graphExecutionCritthash,
             'graphName':               self.mMessage.graphName,
             'graphCycle':              self.mMessage.graphCycle,
             'workExecutionCritthash':  self.mMessage.workExecutionCritthash,
             'workName':                self.mMessage.workName}
        )
        if workExecutionCritthash in aCommandProcessor.mRite.mRecvReq[messageNameRecvReq]:
            aCommandProcessor.mLogger.debug("Delete the received request entry: [%s][%s]." % (messageNameRecvReq, workExecutionCritthash))
            del aCommandProcessor.mRite.mRecvReq[messageNameRecvReq][workExecutionCritthash]
        aCommandProcessor.mLogger.debug("Sending the %s message." % messageNameRecvRes)
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)
