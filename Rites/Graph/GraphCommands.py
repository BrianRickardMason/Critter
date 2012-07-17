"""Graph rite commands."""

from GraphRiteSession import GraphRiteSession

class GraphCommandInitializeGraphExecution(object):
    """InitializeGraphExecution command.

    Attributes:
        mName:    The name of the command.
        mMessage: The ExecuteGraphAnnouncement.

    """

    def __init__(self, aMessage):
        """Initializes the command.

        Arguments:
            aMessage: The ExecuteGraphAnnouncement.

        """
        self.mName    = 'GraphCommandInitializeGraphExecution'
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        """Executes the command.

        Arguments:
            aCommandProcessor: The command processor to be visited.

        """
        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            'DetermineGraphCycleRequest',
            {'sender':    aCommandProcessor.mRite.mCritterData,
             'graphName': self.mMessage.graphName})
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

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
        aCommandProcessor.mRite.mSessions[graphName][graphCycle].mWorkStates[workName] = state
