"""The GraphRiteSession.

Handles a full, single graph execution from the beginning to the end.

"""

import copy
import time
import threading

class GraphRiteSession(threading.Thread):
    """The message processor of the a rite.

    Attributes:
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
        # States of works.
        # 0 - 'Not started'.
        # 1 - 'Started'.
        # 2 - 'Succeed'.
        # 3 - 'Failed'.

        # Set all states of works to 'Not started'.
        for work in self.mWorks:
            self.mWorkStates[work] = 0

        while self.__isCycleActive():
            # Find works to be executed.
            for work in self.mWorks:
                if work in self.mWorkPredecessors:
                    execute = True

                    for workPredecessor in self.mWorkPredecessors[work]:
                        if self.mWorkStates[workPredecessor] == 0:
                            execute = False

                    # Should be executed.
                    if execute:
                        pass

                # Should be executed.
                else:
                    pass

            # TODO: Remove hardcoded value.
            time.sleep(1)

        # Wait for all started jobs.
        # NOTE: The graph was finished with failure status. Collect the rest of the jobs.

        # Delete myself from sessions.
        del self.mRite.mSessions[self.mGraphName][self.mCycle]

    def __isCycleActive(self):
        """Determines whether the cycle is still active (whether there's something to do yet).

        Returns:
            True if something is to be done, False otherwise.

        """
        # FIXME: Remove magic numbers.
        for workState in self.mWorkStates.values():
            if workState == 0 or workState == 1:
                return True

            if workState == 3:
                return False

        return False
