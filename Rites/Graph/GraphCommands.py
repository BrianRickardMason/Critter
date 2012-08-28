"""Graph rite commands."""

from GraphRiteSession import GraphRiteSession

class GraphCommandSpawnGraphExecution(object):
    """SpawnGraphExecution command.

    Attributes:
        mName:    The name of the command.
        mMessage: The DetermineGraphCycleResponse.

    """

    def __init__(self, aMessage):
        """Initializes the command.

        Arguments:
            aMessage: The DetermineGraphCycleResponse.

        """
        self.mName    = 'GraphCommandSpawnGraphExecution'
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        """Executes the command.

        Arguments:
            aCommandProcessor: The command processor to be visited.

        """
        if self.mMessage.receiver.nick == aCommandProcessor.mRite.mCritterData.mNick:
            cycle     = self.mMessage.cycle
            graphName = self.mMessage.graphName

            assert cycle != 0, "Invalid cycle value determined."

            # Create and run a session.
            if graphName not in aCommandProcessor.mRite.mSessions:
                aCommandProcessor.mRite.mSessions[graphName] = {}

            aCommandProcessor.mRite.mSessions[graphName][cycle] = GraphRiteSession(aCommandProcessor.mRite,
                                                                                   graphName,
                                                                                   cycle)
            aCommandProcessor.mRite.mSessions[graphName][cycle].setDaemon(True)
            aCommandProcessor.mRite.mSessions[graphName][cycle].start()
        else:
            aCommandProcessor.mLogger.debug("The message is not addressed to me.")

class GraphCommandLoadGraphAndWork(object):
    """CheckSchedule command.

    Attributes:
        mName:    The name of the command.
        mMessage: The LoadGraphAndWorkResponse.

    """

    def __init__(self, aMessage):
        """Initializes the command.

        Arguments:
            aMessage: The LoadGraphAndWorkResponse.

        """
        self.mName    = "GraphCommandLoadGraphAndWork"
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        """Executes the command.

        Arguments:
            aCommandProcessor: The command processor to be visited.

        """
        # Store graphs.
        for graph in self.mMessage.graphs:
            aCommandProcessor.mRite.mGraphs.append(graph.graphName)

        # Store works.
        for work in self.mMessage.works:
            if work.graphName not in aCommandProcessor.mRite.mWorks:
                aCommandProcessor.mRite.mWorks[work.graphName] = []

            aCommandProcessor.mRite.mWorks[work.graphName].append(work.workName)

        # Store predecessors.
        for predecessor in self.mMessage.workPredecessors:
            if predecessor.workName not in aCommandProcessor.mRite.mWorkPredecessors:
                aCommandProcessor.mRite.mWorkPredecessors[predecessor.workName] = []

            aCommandProcessor.mRite.mWorkPredecessors[predecessor.workName].append(predecessor.predecessorWorkName)

class GraphCommandMarkFinishedWork(object):
    """MarkFinishedWork command.

    Attributes:
        mName:    The name of the command.
        mMessage: The ReportFinishedWorkAnnouncement.

    """

    def __init__(self, aMessage):
        """Initializes the command.

        Arguments:
            aMessage: The ReportFinishedWorkAnnouncement.

        """
        self.mName    = 'GraphCommandMarkFinishedWork'
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        """Executes the command.

        Arguments:
            aCommandProcessor: The command processor to be visited.

        """
        # TODO: Remove hardcoded value.
        if self.mMessage.result == True:
            state = 2
        else:
            state = 3
        state = 2

        graphName  = self.mMessage.graphName
        graphCycle = self.mMessage.graphCycle
        workName   = self.mMessage.workName

        # TODO: Please, do it nicer. Consider holding exceptional cases as well.
        # REMARK: It is possible not to hit the [graphName][graphCycle] entry (e.g. due to a timeout).
        try:
            aCommandProcessor.mRite.mSessions[graphName][graphCycle].mWorkStates[workName] = state
        except KeyError, e:
            pass

class GraphCommand_Handle_ExecuteGraphSeekVolunteers(object):
    def __init__(self, aMessage):
        self.mName = "GraphCommand_Handle_ExecuteGraphSeekVolunteers"
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        hashValue = self.mMessage.hash
        if not hashValue in aCommandProcessor.mRite.mGraphExecutionData:
            aCommandProcessor.mRite.mGraphExecutionData[hashValue] = {}
            aCommandProcessor.mRite.mGraphExecutionData[hashValue]['leadingCriduler'] = self.mMessage.sender.nick

            aCommandProcessor.mLogger.debug("Sending the ExecuteGraphVoluntee.")
            envelope = aCommandProcessor.mRite.mPostOffice.encode(
                'ExecuteGraphVoluntee',
                {'messageName': 'ExecuteGraphVoluntee',
                 'sender':      {'type': aCommandProcessor.mRite.mCritterData.mType,
                                 'nick': aCommandProcessor.mRite.mCritterData.mNick},
                 'receiver':    {'type': self.mMessage.sender.type,
                                 'nick': self.mMessage.sender.nick},
                 'hash':        hashValue})
            aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

        else:
            # TODO: Handle it!
            aCommandProcessor.mLogger.error("Hash is available - conflict.")

class GraphCommand_Handle_ExecuteGraphSelectVolunteer(object):
    def __init__(self, aMessage):
        self.mName = 'GraphCommand_Handle_ExecuteGraphSelectVolunteer'
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            'DetermineGraphCycleRequest',
            {'messageName': 'DetermineGraphCycleRequest',
             'sender':      {'type': aCommandProcessor.mRite.mCritterData.mType,
                             'nick': aCommandProcessor.mRite.mCritterData.mNick},
             'graphName':   self.mMessage.graphName})
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

class GraphCommand_Handle_CommandWorkExecutionSeekVolunteers(object):
    def __init__(self, aMessage):
        self.mName = "GraphCommand_Handle_CommandWorkExecutionSeekVolunteers"
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        hashValue = self.mMessage.hash
        if hashValue in aCommandProcessor.mRite.mCommandWorkExecutionVolunteering:
            aCommandProcessor.mLogger.debug("Storing CommandWorkExecution volunteering data under a hash: %s." % hashValue)
            aCommandProcessor.mRite.mCommandWorkExecutionVolunteering[hashValue]['boss'] = self.mMessage.sender.nick
        else:
            aCommandProcessor.mLogger.warn("Hash is unavailable.")

class GraphCommand_Handle_CommandWorkExecutionVoluntee(object):
    def __init__(self, aMessage):
        self.mName = "GraphCommand_Handle_CommandWorkExecutionVoluntee"
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mCritter.mCritterData.mType != self.mMessage.receiver.type or \
           aCommandProcessor.mRite.mCritter.mCritterData.mNick != self.mMessage.receiver.nick    :
            aCommandProcessor.mLogger.debug("The message is not addressed to me.")
            return

        hashValue = self.mMessage.hash

        if not hashValue in aCommandProcessor.mRite.mCommandWorkExecutionVolunteering:
            aCommandProcessor.mLogger.warn("The hash is unavailable.")
            return

        if 'worker' in aCommandProcessor.mRite.mCommandWorkExecutionVolunteering[hashValue]:
            aCommandProcessor.mLogger.debug("Leading worker has already been selected.")
            return

        aCommandProcessor.mLogger.debug("Storing CommandWorkExecution volunteering data under a hash: %s." % hashValue)
        aCommandProcessor.mRite.mCommandWorkExecutionVolunteering[hashValue]['worker'] = self.mMessage.sender.nick

        aCommandProcessor.mLogger.debug("Sending the CommandWorkExecutionSelectVolunteer message.")
        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            'CommandWorkExecutionSelectVolunteer',
            {'messageName': 'CommandWorkExecutionSelectVolunteer',
             'sender':      {'type': aCommandProcessor.mRite.mCritterData.mType,
                             'nick': aCommandProcessor.mRite.mCritterData.mNick},
             'receiver':    {'type': self.mMessage.sender.type,
                             'nick': self.mMessage.sender.nick},
             'hash':        hashValue,
             'graphName':   aCommandProcessor.mRite.mCommandWorkExecutionVolunteering[hashValue]['graphName'],
             'graphCycle':  aCommandProcessor.mRite.mCommandWorkExecutionVolunteering[hashValue]['graphCycle'],
             'workName':    aCommandProcessor.mRite.mCommandWorkExecutionVolunteering[hashValue]['workName']})
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)
