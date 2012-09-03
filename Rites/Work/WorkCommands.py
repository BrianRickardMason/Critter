from WorkRiteSession import WorkRiteSession

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

class WorkCommand_Handle_Command_ExecuteWork_Req(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if    aCommandProcessor.mRite.mCritter.mCritterData.mNick \
           == self.mMessage.receiverCrittnick:
            aCommandProcessor.mLogger.debug("I have been selected.")

            workExecutionCritthash = self.mMessage.workExecutionCritthash

            messageName = self.mMessage.messageName
            aCommandProcessor.mRite.insertRecvRequest(messageName, workExecutionCritthash, self.mMessage)

            messageName = 'Command_DetermineWorkCycle_Req'
            envelope = aCommandProcessor.mRite.mPostOffice.encode(
                messageName,
                {'messageName':             messageName,
                 'graphExecutionCritthash': self.mMessage.graphExecutionCritthash,
                 'graphName':               self.mMessage.graphName,
                 'graphCycle':              self.mMessage.graphCycle,
                 'workExecutionCritthash':  self.mMessage.workExecutionCritthash,
                 'workName':                self.mMessage.workName}
            )
            aCommandProcessor.mRite.insertSentRequest(messageName, workExecutionCritthash, envelope)

class WorkCommand_Handle_Command_DetermineWorkCycle_Res(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        workExecutionCritthash = self.mMessage.workExecutionCritthash

        messageNameSentReq = 'Command_DetermineWorkCycle_Req'
        if workExecutionCritthash in aCommandProcessor.mRite.mSentReq[messageNameSentReq]:
            aCommandProcessor.mRite.deleteSentRequest(messageNameSentReq, workExecutionCritthash)

            graphCycle = self.mMessage.graphCycle
            workCycle  = self.mMessage.workCycle
            workName   = self.mMessage.workName

            assert graphCycle > 0, "Invalid graphCycle value determined."
            assert workCycle  > 0, "Invalid workCycle value determined."

            # Create and run a session.
            if workName not in aCommandProcessor.mRite.mSessions:
                aCommandProcessor.mRite.mSessions[workName] = {}

            aCommandProcessor.mRite.mSessions[workName][workCycle] = WorkRiteSession(aCommandProcessor.mRite,
                                                                                     self.mMessage.graphExecutionCritthash,
                                                                                     self.mMessage.graphName,
                                                                                     graphCycle,
                                                                                     workExecutionCritthash,
                                                                                     workName,
                                                                                     workCycle)
            aCommandProcessor.mRite.mSessions[workName][workCycle].setDaemon(True)
            aCommandProcessor.mRite.mSessions[workName][workCycle].start()
