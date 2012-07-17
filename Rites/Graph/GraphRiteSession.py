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
        # TODO: Remove hardcoded values.
        # States of works.
        # 0 - 'Not started'.
        # 1 - 'Started'.
        # 2 - 'Succeed'.
        # 3 - 'Failed'.

        # Set all states of works to 'Not started'.
        for work in self.mWorks:
            self.mWorkStates[work] = 0

        # Spawn works to be executed.
        spawnChecker = SpawnChecker()

        while spawnChecker.continueSpawning(self.mWorkStates):
            # Browse all works.
            for work in self.mWorks:
                # Work is in 'Not started' state.
                if self.mWorkStates[work] == 0:
                    if work in self.mWorkPredecessors:
                        execute = True

                        for workPredecessor in self.mWorkPredecessors[work]:
                            if self.mWorkStates[workPredecessor] in [0, 1, 3]:
                                execute = False

                        # Should be executed.
                        if execute:
                            self.__commandWorkExecutionAnnouncement(work)

                    # Should be executed.
                    else:
                        self.__commandWorkExecutionAnnouncement(work)

            # TODO: Remove hardcoded value.
            time.sleep(1)

        # Wait for all started jobs to finish.
        awaiter = Awaiter()

        while awaiter.keepWaiting(self.mWorkStates):
            # TODO: Remove hardcoded value.
            time.sleep(1)

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
        self.mWorkStates[aWorkName] = 1

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
        # There's the 'Failed' state.
        if 3 in aWorkStates.values():
            return False

        # There are only 'Started' states.
        onlyStarted = True
        for workState in aWorkStates.values():
            if workState != 1:
                onlyStarted = False
        if onlyStarted == True:
            return False

        # There are only 'Started' and 'Succeed' states.
        onlyStartedAndSucceed = True
        for workState in aWorkStates.values():
            if workState not in [1, 2]:
                onlyStartedAndSucceed = False
        if onlyStartedAndSucceed == True:
            return False

        # There are only 'Not started' and 'Started' and 'Succeed' states.
        return True

class Awaiter(object):
    """Check whether there's a need to keep waiting until all jobs are completed."""

    def keepWaiting(self, aWorkStates):
        """Checks whether or not to keep waiting until all jobs are completed.

        Arguments:
            aWorkStates: The dictionary of work states.

        Returns:
            True if there's a need to keep waiting, False otherwise.

        """
        # There's the 'Started' state.
        if 1 in aWorkStates.values():
            return True

        return False
