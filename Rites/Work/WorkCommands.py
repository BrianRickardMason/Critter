"""Work rite commands."""

from WorkRiteSession import WorkRiteSession

class WorkCommandInitializeWorkExecution(object):
    """InitializeWorkExecution command.

    Attributes:
        mName:    The name of the command.
        mMessage: The ExecuteWorkAnnouncement.

    """

    def __init__(self, aMessage):
        """Initializes the command.

        Arguments:
            aMessage: The ExecuteWorkAnnouncement.

        """
        self.mName    = 'WorkCommandInitializeWorkExecution'
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        """Executes the command.

        Arguments:
            aCommandProcessor: The command processor to be visited.

        """
        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            'DetermineWorkCycleRequest',
            {'messageName': 'DetermineWorkCycleRequest',
             'sender':      {'type': aCommandProcessor.mRite.mCritterData.mType,
                             'nick': aCommandProcessor.mRite.mCritterData.mNick},
             'graphName':   self.mMessage.graphName,
             'cycle':       self.mMessage.cycle,
             'workName':    self.mMessage.workName})
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

class WorkCommandSpawnWorkExecution(object):
    """SpawnWorkExecution command.

    Attributes:
        mName:    The name of the command.
        mMessage: The DetermineWorkCycleResponse.

    """

    def __init__(self, aMessage):
        """Initializes the command.

        Arguments:
            aMessage: The DetermineWorkCycleResponse.

        """
        self.mName    = 'WorkCommandSpawnWorkExecution'
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        """Executes the command.

        Arguments:
            aCommandProcessor: The command processor to be visited.

        """
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
#
            aCommandProcessor.mRite.mSessions[workName][workCycle] = WorkRiteSession(aCommandProcessor.mRite,
                                                                                     graphName,
                                                                                     graphCycle,
                                                                                     workName,
                                                                                     workCycle)
            aCommandProcessor.mRite.mSessions[workName][workCycle].setDaemon(True)
            aCommandProcessor.mRite.mSessions[workName][workCycle].start()
        else:
            aCommandProcessor.mLogger.debug("The message is not addressed to me.")
