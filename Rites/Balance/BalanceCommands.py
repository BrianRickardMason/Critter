from random import choice

import Rites.RiteCommon

from Critter.CritterData import CritterData

class BalanceCommand_Handle_CommandWorkExecutionSeekVolunteers(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        hashValue = self.mMessage.hash
        if hashValue in aCommandProcessor.mRite.mCommandWorkExecutionVolunteering:
            # TODO: Handle it!
            aCommandProcessor.mLogger.error("Hash is available - conflict.")
            return

        aCommandProcessor.mLogger.debug("Storing CommandWorkExecution volunteering data under a hash: %s." % hashValue)
        aCommandProcessor.mRite.mCommandWorkExecutionVolunteering[hashValue] = {}
        aCommandProcessor.mRite.mCommandWorkExecutionVolunteering[hashValue]['boss'] = self.mMessage.sender.nick

        aCommandProcessor.mLogger.debug("Sending the CommandWorkExecutionVoluntee message.")
        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            'CommandWorkExecutionVoluntee',
            {'messageName': 'CommandWorkExecutionVoluntee',
             'sender':      {'type': aCommandProcessor.mRite.mCritterData.mType,
                             'nick': aCommandProcessor.mRite.mCritterData.mNick},
             'receiver':    {'type': self.mMessage.sender.type,
                             'nick': self.mMessage.sender.nick},
             'hash':        hashValue})
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

class BalanceCommand_Handle_CommandWorkExecutionSelectVolunteer(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mCritter.mCritterData.mType != self.mMessage.receiver.type or \
           aCommandProcessor.mRite.mCritter.mCritterData.mNick != self.mMessage.receiver.nick    :
            aCommandProcessor.mLogger.debug("The message is not addressed to me.")
            return

        hashValue = self.mMessage.hash

        aCommandProcessor.mLogger.debug("Storing CommandWorkExecution volunteering data under a hash: %s." % hashValue)
        aCommandProcessor.mRite.mCommandWorkExecutionVolunteering[hashValue] = {}
        aCommandProcessor.mRite.mCommandWorkExecutionVolunteering[hashValue]['graphName']  = self.mMessage.graphName
        aCommandProcessor.mRite.mCommandWorkExecutionVolunteering[hashValue]['graphCycle'] = self.mMessage.graphCycle
        aCommandProcessor.mRite.mCommandWorkExecutionVolunteering[hashValue]['workName']   = self.mMessage.workName
        aCommandProcessor.mRite.mCommandWorkExecutionVolunteering[hashValue]['worker']     = self.mMessage.receiver.nick

        # Get the list of known critters.
        # FIXME: Jealous class.
        knownCritters = aCommandProcessor.mRite.mCritter.mRites[Rites.RiteCommon.REGISTRY].getKnownCritters()

        # Filter workers.
        availableWorkers = []
        for critterData in knownCritters.values():
            if critterData.mType == 'Worker':
                availableWorkers.append(critterData.mNick)

        # Balance the load.
        # FIXME: What happens when there are not any workers?
        foundWorker = choice(availableWorkers)

        # Command work execution.
        # FIXME: Remove hardcodes.
        foundWorkerData = CritterData('Worker', foundWorker)

        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            'ExecuteWorkAnnouncement',
            {'messageName': 'ExecuteWorkAnnouncement',
             'sender':      {'type': aCommandProcessor.mRite.mCritterData.mType,
                             'nick': aCommandProcessor.mRite.mCritterData.mNick},
             'receiver':    {'type': foundWorkerData.mType,
                             'nick': foundWorkerData.mNick},
             'graphName':   self.mMessage.graphName,
             'cycle':       self.mMessage.graphCycle,
             'workName':    self.mMessage.workName})
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

class BalanceCommand_Handle_Command_Req_OrderWorkExecution(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        workExecutionCritthash = self.mMessage.workExecutionCritthash

        assert workExecutionCritthash not in aCommandProcessor.mRite.mRecvReq['Command_Req_OrderWorkExecution'], "Not handled yet. Duplicated critthash."
        aCommandProcessor.mLogger.debug("Insert the received request entry: [%s][%s]." % ('Command_Req_OrderWorkExecution', workExecutionCritthash))
        aCommandProcessor.mRite.mRecvReq['Command_Req_OrderWorkExecution'][workExecutionCritthash] = self.mMessage

        assert workExecutionCritthash not in aCommandProcessor.mRite.mElections, "Not handled yet. Duplicated critthash."
        aCommandProcessor.mLogger.debug("Insert the election entry: [%s]." % workExecutionCritthash)
        aCommandProcessor.mRite.mElections[workExecutionCritthash] = {'message': self.mMessage}

        messageName = 'Command_Req_Election'
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

class BalanceCommand_Handle_Command_Req_OrderWorkExecution_ElectionFinished(object):
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

            messageName = 'Command_Req_ExecuteWork'
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

class BalanceCommand_Handle_Command_Res_Election(object):
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
                aCommandProcessor.mLogger.debug("Update the election entry: [%s]." % critthash)
                aCommandProcessor.mRite.mElections[critthash]['crittnick'] = self.mMessage.crittnick

                assert 'message' in aCommandProcessor.mRite.mElections[critthash], "There's no information about the message."
                message = aCommandProcessor.mRite.mElections[critthash]['message']

                # Handle the election topic.
                if message.messageName == 'Command_Req_OrderWorkExecution':
                    command = BalanceCommand_Handle_Command_Req_OrderWorkExecution_ElectionFinished(message)
                    aCommandProcessor.mRite.mPostOffice.putCommand(Rites.RiteCommon.BALANCE, command)
