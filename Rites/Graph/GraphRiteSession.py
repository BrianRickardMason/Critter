import copy
import logging
import os
import time
import threading

logging.basicConfig(format='[%(asctime)s][%(threadName)28s][%(levelname)8s] - %(message)s')

# TODO: Introduce a graph timeout.
# TODO: Consider introduction of a work timeout.
# FIXME: Many threads access work states.

class GraphRiteSession(threading.Thread):
    SLEEP_BETWEEN_SPAWNING = 1 # [s].
    SLEEP_WHILE_WAITING    = 1 # [s].

    STATE_NOT_STARTED = 0
    STATE_STARTED     = 1
    STATE_SUCCEED     = 2
    STATE_FAILED      = 3

    def __init__(self, aRite, aGraphExecutionCritthash, aGraphName, aGraphCycle):
        self.mLogger = logging.getLogger('GraphRiteSession')
        self.mLogger.setLevel(logging.INFO)

        self.mRite                    = aRite
        self.mGraphExecutionCritthash = aGraphExecutionCritthash
        self.mGraphName               = aGraphName
        self.mGraphCycle              = aGraphCycle

        assert aGraphName in self.mRite.mWorks, "The graph name has not any works associated."

        self.mWorks            = copy.deepcopy(self.mRite.mWorks[aGraphName])
        self.mWorkPredecessors = aRite.mWorkPredecessors

        self.mWorkStates = {}

        threading.Thread.__init__(self, name='GraphRiteSession')

    def run(self):
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
        del self.mRite.mSessions[self.mGraphName][self.mGraphCycle]

    def __commandWorkExecutionAnnouncement(self, aWorkName):
        self.mLogger.info("Ordering a work execution: %s@%s@%s." % (self.mGraphName, self.mGraphCycle, aWorkName))

        # Set the state.
        self.mWorkStates[aWorkName] = self.STATE_STARTED

        if    self.mRite.mCritter.mCritterData.mNick \
           == self.mRite.mElections[self.mGraphExecutionCritthash]['crittnick']:

            workExecutionCritthash = os.urandom(32).encode('hex')

            envelope = self.mRite.mPostOffice.encode(
                'Command_Req_OrderWorkExecution',
                {'messageName':             'Command_Req_OrderWorkExecution',
                 'graphExecutionCritthash': self.mGraphExecutionCritthash,
                 'graphName':               self.mGraphName,
                 'graphCycle':              self.mGraphCycle,
                 'workExecutionCritthash':  workExecutionCritthash,
                 'workName':                aWorkName}
            )
            assert workExecutionCritthash not in self.mRite.mSentReq['Command_Req_OrderWorkExecution'], "Not handled yet. Duplicated critthash."
            self.mLogger.debug("Insert the sent request entry: [%s][%s]." % ('Command_Req_OrderWorkExecution', workExecutionCritthash))
            self.mRite.mSentReq['Command_Req_OrderWorkExecution'][workExecutionCritthash] = envelope
            self.mLogger.debug("Sending the Command_Req_OrderWorkExecution message.")
            self.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

class SpawnChecker(object):
    def continueSpawning(self, aWorkStates):
        # There's the 'STATE_FAILED' state.
        if GraphRiteSession.STATE_FAILED in aWorkStates.values():
            return False

        # There are only STATE_STARTED' states.
        onlyStateStarted = True
        for workState in aWorkStates.values():
            if workState not in [GraphRiteSession.STATE_STARTED]:
                onlyStateStarted = False
        if onlyStateStarted == True:
            return False

        # There are only 'STATE_STARTED' and 'STATE_SUCCEED' states.
        onlyStateStartedAndStateSucceed = True
        for workState in aWorkStates.values():
            if workState not in [GraphRiteSession.STATE_STARTED,
                                 GraphRiteSession.STATE_SUCCEED]:
                onlyStateStartedAndStateSucceed = False
        if onlyStateStartedAndStateSucceed == True:
            return False

        # There are only 'STATE_NOT_STARTED' and STATE_STARTED' and 'STATE_SUCCEED' states.
        return True

class WorkFinder(object):
    def __init__(self, aWorks, aWorkPredecessors):
        self.mWorks            = aWorks
        self.mWorkPredecessors = aWorkPredecessors

    def findWorks(self, aWorkStates):
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
    def keepWaiting(self, aWorkStates):
        # There's the 'STATE_STARTED' state.
        if GraphRiteSession.STATE_STARTED in aWorkStates.values():
            return True

        return False
