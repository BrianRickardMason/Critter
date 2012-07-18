"""The GraphRiteSession.

Handles a full, single graph execution from the beginning to the end.

"""

import copy
import logging
import time
import threading

logging.basicConfig(format='[%(asctime)s][%(threadName)28s][%(levelname)8s] - %(message)s')

# TODO: Introduce a graph timeout.
# TODO: Consider introduction of a work timeout.
# FIXME: Many threads access work states.

class GraphRiteSession(threading.Thread):
    """The message processor of the a rite.

    Attributes:
        mLogger:           The logger.
        mRite:             The rite.
        mGraphName:        The graph name.
        mCycle:            The cycle number.
        mWorks:            Keeps the available works.
        mWorkPredecessors: Keeps the predecessors of the works.
        mWorkStates:       Keeps the states of works.

    """

    SLEEP_BETWEEN_SPAWNING = 1 # [s].
    SLEEP_WHILE_WAITING    = 1 # [s].

    STATE_NOT_STARTED = 0
    STATE_STARTED     = 1
    STATE_SUCCEED     = 2
    STATE_FAILED      = 3

    def __init__(self, aRite, aGraphName, aCycle):
        """Initializes the message processor.

        Arguments:
            aRite:      The rite.
            aGraphName: The graph name.
            aCycle:     The cycle number.

        """
        self.mLogger = logging.getLogger('GraphRiteSession')
        self.mLogger.setLevel(logging.INFO)

        self.mRite      = aRite
        self.mGraphName = aGraphName
        self.mCycle     = aCycle

        assert aGraphName in self.mRite.mWorks, "The graph name has not any works associated."

        self.mWorks            = copy.deepcopy(self.mRite.mWorks[aGraphName])
        self.mWorkPredecessors = aRite.mWorkPredecessors

        self.mWorkStates = {}

        threading.Thread.__init__(self, name='GraphRiteSession')

    def run(self):
        """Starts the main loop of the session."""
        # Set all states of works to 'STATE_NOT_STARTED'.
        for work in self.mWorks:
            self.mWorkStates[work] = GraphRiteSession.STATE_NOT_STARTED

        spawnChecker = SpawnChecker()
        workFinder   = WorkFinder(self.mWorks, self.mWorkPredecessors)

        # Spawn works to be executed.
        while spawnChecker.continueSpawning(self.mWorkStates):
            # Find works to be started.
            worksToBeStarted = workFinder.findWorks(self.mWorkStates)

            # Start works.
            for work in worksToBeStarted:
                self.__commandWorkExecutionAnnouncement(work)

            time.sleep(GraphRiteSession.SLEEP_BETWEEN_SPAWNING)

        awaiter = Awaiter()

        # Wait for all started jobs to finish.
        while awaiter.keepWaiting(self.mWorkStates):
            time.sleep(GraphRiteSession.SLEEP_WHILE_WAITING)

        # Delete myself from sessions.
        del self.mRite.mSessions[self.mGraphName][self.mCycle]

    def __commandWorkExecutionAnnouncement(self, aWorkName):
        """Commands the work execution.

        Arguments:
            aWorkName: The name of the work.

        """
        self.mLogger.info("Commanding work execution: %s@%s@%s." % (self.mGraphName, self.mCycle, aWorkName))

        assert aWorkName in self.mWorkStates, "Work %s has not its state attached." % aWorkName

        # Set the state.
        self.mWorkStates[aWorkName] = GraphRiteSession.STATE_STARTED

        # Send the message.
        envelope = self.mRite.mPostOffice.encode(
            'CommandWorkExecutionAnnouncement',
            {'sender':    self.mRite.mCritterData,
             'graphName': self.mGraphName,
             'cycle':     self.mCycle,
             'workName':  aWorkName})
        self.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

class SpawnChecker(object):
    """Checks whether there's a need to continue spawning works."""

    def continueSpawning(self, aWorkStates):
        """Checks whether or not to continue spawning works.

        Arguments:
            aWorkStates: The dictionary of work states.

        Returns:
            True if there's a need to continue spawning, False otherwise.

        """
        # There's the 'STATE_FAILED' state.
        if GraphRiteSession.STATE_FAILED in aWorkStates.values():
            return False

        # There are only 'STATE_STARTED' states.
        onlyStateStarted = True
        for workState in aWorkStates.values():
            if workState != GraphRiteSession.STATE_STARTED:
                onlyStateStarted = False
        if onlyStateStarted == True:
            return False

        # There are only 'STATE_STARTED' and 'STATE_SUCCEED' states.
        onlyStateStartedAndStateSucceed = True
        for workState in aWorkStates.values():
            if workState not in [GraphRiteSession.STATE_STARTED, GraphRiteSession.STATE_SUCCEED]:
                onlyStateStartedAndStateSucceed = False
        if onlyStateStartedAndStateSucceed == True:
            return False

        # There are only 'STATE_NOT_STARTED' and 'STATE_STARTED' and 'STATE_SUCCEED' states.
        return True

class WorkFinder(object):
    """Finds the works that should be spawned.

    Attributes:
        mWorks:            Keeps the available works.
        mWorkPredecessors: Keeps the predecessors of the works.

    """

    def __init__(self, aWorks, aWorkPredecessors):
        """Initializes the finder.

        Arguments:
            aWorks:            Keeps the available works.
            aWorkPredecessors: Keeps the predecessors of the works.

        """
        self.mWorks            = aWorks
        self.mWorkPredecessors = aWorkPredecessors

    def findWorks(self, aWorkStates):
        """Finds the works that should be started.

        Arguments:
            aWorkStates: Keeps the states of works.

        Returns:
            The array of works that should be started.

        """
        worksToBeStarted = []

        for work in self.mWorks:
            # The work is in 'STATE_NOT_STARTED' state.
            if aWorkStates[work] == GraphRiteSession.STATE_NOT_STARTED:
                # The work has predecessors.
                if work in self.mWorkPredecessors:
                    # The work wants to be executed...
                    execute = True

                    # ...and only if any of its predecessors is not in 'STATE_SUCCEED' can stop it.
                    for workPredecessor in self.mWorkPredecessors[work]:
                        if aWorkStates[workPredecessor] != GraphRiteSession.STATE_SUCCEED:
                            execute = False

                    # Should be executed.
                    if execute:
                        worksToBeStarted.append(work)

                # Work has not predecessors.
                # Should be executed.
                else:
                    worksToBeStarted.append(work)

        return worksToBeStarted

class Awaiter(object):
    """Check whether there's a need to keep waiting until all jobs are completed."""

    def keepWaiting(self, aWorkStates):
        """Checks whether or not to keep waiting until all jobs are completed.

        Arguments:
            aWorkStates: The dictionary of work states.

        Returns:
            True if there's a need to keep waiting, False otherwise.

        """
        # There's the 'STATE_STARTED' state.
        if GraphRiteSession.STATE_STARTED in aWorkStates.values():
            return True

        return False
