from WorkRiteSession import WorkRiteSession

class WorkCommandInitializeWorkExecution(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mCritter.mCritterData.mType == self.mMessage.sender.type and \
           aCommandProcessor.mRite.mCritter.mCritterData.mNick == self.mMessage.sender.nick     :
            return

        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            'DetermineWorkCycleRequest',
            {'messageName': 'DetermineWorkCycleRequest',
             'sender':      {'type': aCommandProcessor.mRite.mCritterData.mType,
                             'nick': aCommandProcessor.mRite.mCritterData.mNick},
             'graphName':   self.mMessage.graphName,
             'cycle':       self.mMessage.cycle,
             'workName':    self.mMessage.workName})
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

class WorkCommandLoadWorkDetails(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mCritter.mCritterData.mType == self.mMessage.sender.type and \
           aCommandProcessor.mRite.mCritter.mCritterData.mNick == self.mMessage.sender.nick     :
            return

        # Store work details.
        for workDetail in self.mMessage.details:
            aCommandProcessor.mRite.mWorkDetails[workDetail.workName] = {'workName': workDetail.workName,
                                                                         'dummy':    workDetail.dummy}

class WorkCommandSpawnWorkExecution(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mCritter.mCritterData.mType == self.mMessage.sender.type and \
           aCommandProcessor.mRite.mCritter.mCritterData.mNick == self.mMessage.sender.nick     :
            return

        if self.mMessage.receiver.nick == aCommandProcessor.mRite.mCritterData.mNick:
            graphName  = self.mMessage.graphName
            # FIXME: Should be self.mMessage.workCycle.
            graphCycle = self.mMessage.cycle
            workName   = self.mMessage.workName
            workCycle  = self.mMessage.workCycle

            assert graphCycle > 0, "Invalid graphCycle value determined."
            assert workCycle  > 0, "Invalid workCycle value determined."

            # Create and run a session.
            if workName not in aCommandProcessor.mRite.mSessions:
                aCommandProcessor.mRite.mSessions[workName] = {}

            aCommandProcessor.mRite.mSessions[workName][workCycle] = WorkRiteSession(aCommandProcessor.mRite,
                                                                                     graphName,
                                                                                     graphCycle,
                                                                                     workName,
                                                                                     workCycle)
            aCommandProcessor.mRite.mSessions[workName][workCycle].setDaemon(True)
            aCommandProcessor.mRite.mSessions[workName][workCycle].start()
        else:
            aCommandProcessor.mLogger.debug("The message is not addressed to me.")

class WorkCommand_Handle_Command_Req_ExecuteWork(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if    aCommandProcessor.mRite.mCritter.mCritterData.mNick \
           == self.mMessage.receiverCrittnick:
            aCommandProcessor.mLogger.debug("I have been selected.")

            workExecutionCritthash = self.mMessage.workExecutionCritthash

            messageName = 'Command_Req_ExecuteWork'
            assert workExecutionCritthash not in aCommandProcessor.mRite.mRecvReq[messageName], "Not handled yet. Duplicated critthash."
            aCommandProcessor.mLogger.debug("Insert the received request entry: [%s][%s]." % (messageName, workExecutionCritthash))
            aCommandProcessor.mRite.mRecvReq[messageName][workExecutionCritthash] = self.mMessage

            messageName = 'Command_Req_DetermineWorkCycle'
            envelope = aCommandProcessor.mRite.mPostOffice.encode(
                messageName,
                {'messageName':             messageName,
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
