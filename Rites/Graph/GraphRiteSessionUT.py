"""Unit tests."""

import unittest

from GraphRiteSession import Awaiter
from GraphRiteSession import GraphRiteSession
from GraphRiteSession import SpawnChecker

class SpawnChecker_ContinueSpawning(unittest.TestCase):

    def setUp(self):
        self.mSpawnChecker = SpawnChecker()

    def testContinueSpawningReturnsTrueIfThereIsOnlyOneNotStartedState(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_NOT_STARTED
        }
        self.assertTrue(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsFalseIfThereIsOnlyOneStartedState(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_STARTED
        }
        self.assertFalse(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsFalseIfThereIsOnlyOneSucceedState(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_SUCCEED
        }
        self.assertFalse(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsFalseIfThereIsOnlyOneFailedState(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_FAILED
        }
        self.assertFalse(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsTrueIfThereAreOnlyNotStartedStates(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_NOT_STARTED,
            'Work2': GraphRiteSession.STATE_NOT_STARTED,
            'Work3': GraphRiteSession.STATE_NOT_STARTED,
            'Work4': GraphRiteSession.STATE_NOT_STARTED
        }
        self.assertTrue(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsFalseIfThereAreOnlyStartedStates(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_STARTED,
            'Work2': GraphRiteSession.STATE_STARTED,
            'Work3': GraphRiteSession.STATE_STARTED,
            'Work4': GraphRiteSession.STATE_STARTED
        }
        self.assertFalse(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsFalseIfThereAreOnlySucceedStates(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_SUCCEED,
            'Work2': GraphRiteSession.STATE_SUCCEED,
            'Work3': GraphRiteSession.STATE_SUCCEED,
            'Work4': GraphRiteSession.STATE_SUCCEED
        }
        self.assertFalse(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsFalseIfThereAreOnlyFailedStates(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_FAILED,
            'Work2': GraphRiteSession.STATE_FAILED,
            'Work3': GraphRiteSession.STATE_FAILED,
            'Work4': GraphRiteSession.STATE_FAILED
        }
        self.assertFalse(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsTrueIfThereAreOnlyNotStartedAndStartedStates_OneNotStartedOneStarted(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_NOT_STARTED,
            'Work2': GraphRiteSession.STATE_STARTED
        }
        self.assertTrue(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsTrueIfThereAreOnlyNotStartedAndStartedStates_ManyNotStartedOneStarted(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_NOT_STARTED,
            'Work2': GraphRiteSession.STATE_NOT_STARTED,
            'Work3': GraphRiteSession.STATE_STARTED,
            'Work4': GraphRiteSession.STATE_NOT_STARTED
        }
        self.assertTrue(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsTrueIfThereAreOnlyNotStartedAndStartedStates_OneNotStartedManyStarted(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_STARTED,
            'Work2': GraphRiteSession.STATE_STARTED,
            'Work3': GraphRiteSession.STATE_NOT_STARTED,
            'Work4': GraphRiteSession.STATE_STARTED
        }
        self.assertTrue(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsTrueIfThereAreOnlyNotStartedAndSucceedStates_OneNotStartedOneSucceed(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_NOT_STARTED,
            'Work2': GraphRiteSession.STATE_SUCCEED
        }
        self.assertTrue(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsTrueIfThereAreOnlyNotStartedAndSucceedStates_ManyNotStartedOneSucceed(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_NOT_STARTED,
            'Work2': GraphRiteSession.STATE_NOT_STARTED,
            'Work3': GraphRiteSession.STATE_SUCCEED,
            'Work4': GraphRiteSession.STATE_NOT_STARTED
        }
        self.assertTrue(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsTrueIfThereAreOnlyNotStartedAndSucceedStates_OneNotStartedManySucceed(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_SUCCEED,
            'Work2': GraphRiteSession.STATE_SUCCEED,
            'Work3': GraphRiteSession.STATE_NOT_STARTED,
            'Work4': GraphRiteSession.STATE_SUCCEED
        }
        self.assertTrue(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsTrueIfThereAreOnlyOneNotStartedAndStartedAndSucceedStates_OneNotStartedManyStartedManySuceed(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_STARTED,
            'Work2': GraphRiteSession.STATE_SUCCEED,
            'Work3': GraphRiteSession.STATE_STARTED,
            'Work4': GraphRiteSession.STATE_SUCCEED,
            'Work5': GraphRiteSession.STATE_NOT_STARTED
        }
        self.assertTrue(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsFalseIfThereAreOnlyStartedAndSucceedStates_OneStartedOneSucceed(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_STARTED,
            'Work2': GraphRiteSession.STATE_SUCCEED
        }
        self.assertFalse(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsFalseIfThereAreOnlyStartedAndSucceedStates_ManyStartedManySucceed(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_STARTED,
            'Work2': GraphRiteSession.STATE_SUCCEED,
            'Work3': GraphRiteSession.STATE_STARTED,
            'Work4': GraphRiteSession.STATE_SUCCEED,
            'Work5': GraphRiteSession.STATE_STARTED
        }
        self.assertFalse(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsFalseIfThereIsAFailedState(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_NOT_STARTED,
            'Work2': GraphRiteSession.STATE_FAILED
        }
        self.assertFalse(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsFalseIfThereAreOnlyStartedAndFailedStates(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_STARTED,
            'Work2': GraphRiteSession.STATE_FAILED,
            'Work3': GraphRiteSession.STATE_STARTED
        }
        self.assertFalse(self.mSpawnChecker.continueSpawning(workStates))

class Awaiter_KeepWaiting(unittest.TestCase):

    def setUp(self):
        self.mAwaiter = Awaiter()

    def testKeepWaitingReturnsFalseIfThereIsOnlyOneNotStartedState(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_NOT_STARTED
        }
        self.assertFalse(self.mAwaiter.keepWaiting(workStates))

    def testKeepWaitingReturnsTrueIfThereIsOnlyOneStartedState(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_STARTED
        }
        self.assertTrue(self.mAwaiter.keepWaiting(workStates))

    def testKeepWaitingReturnsFalseIfThereIsOnlyOneSucceedState(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_SUCCEED
        }
        self.assertFalse(self.mAwaiter.keepWaiting(workStates))

    def testKeepWaitingReturnsFalseIfThereIsOnlyOneFailedState(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_FAILED
        }
        self.assertFalse(self.mAwaiter.keepWaiting(workStates))

    def testKeepWaitingReturnsFalseIfThereAreOnlyNotStartedStates(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_NOT_STARTED,
            'Work2': GraphRiteSession.STATE_NOT_STARTED,
            'Work3': GraphRiteSession.STATE_NOT_STARTED,
            'Work4': GraphRiteSession.STATE_NOT_STARTED
        }
        self.assertFalse(self.mAwaiter.keepWaiting(workStates))

    def testKeepWaitingReturnsTrueIfThereAreOnlyStartedStates(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_STARTED,
            'Work2': GraphRiteSession.STATE_STARTED,
            'Work3': GraphRiteSession.STATE_STARTED,
            'Work4': GraphRiteSession.STATE_STARTED
        }
        self.assertTrue(self.mAwaiter.keepWaiting(workStates))

    def testKeepWaitingReturnsFalseIfThereAreOnlySucceedStates(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_FAILED,
            'Work2': GraphRiteSession.STATE_FAILED,
            'Work3': GraphRiteSession.STATE_FAILED,
            'Work4': GraphRiteSession.STATE_FAILED
        }
        self.assertFalse(self.mAwaiter.keepWaiting(workStates))

    def testKeepWaitingReturnsFalseIfThereAreOnlyFailedStates(self):
        workStates = \
        {
            'Work1': 4,
            'Work2': 4,
            'Work3': 4,
            'Work4': 4
        }
        self.assertFalse(self.mAwaiter.keepWaiting(workStates))

    def testKeepAwaitingReturnsTrueIfThereAreStartedStates_OneStartedOneAnother(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_NOT_STARTED,
            'Work2': GraphRiteSession.STATE_STARTED
        }
        self.assertTrue(self.mAwaiter.keepWaiting(workStates))

    def testKeepAwaitingReturnsTrueIfThereAreStartedStates_OneStartedManyAnother(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_STARTED,
            'Work2': GraphRiteSession.STATE_SUCCEED,
            'Work3': GraphRiteSession.STATE_FAILED,
            'Work4': GraphRiteSession.STATE_NOT_STARTED
        }
        self.assertTrue(self.mAwaiter.keepWaiting(workStates))

    def testKeepAwaitingReturnsTrueIfThereAreStartedStates_ManyStartedOneAnother(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_STARTED,
            'Work2': GraphRiteSession.STATE_STARTED,
            'Work3': GraphRiteSession.STATE_FAILED,
            'Work4': GraphRiteSession.STATE_STARTED
        }
        self.assertTrue(self.mAwaiter.keepWaiting(workStates))

    def testKeepAwaitingReturnsTrueIfThereAreStartedStates_ManyStartedManyAnother(self):
        workStates = \
        {
            'Work1': GraphRiteSession.STATE_STARTED,
            'Work2': GraphRiteSession.STATE_SUCCEED,
            'Work3': GraphRiteSession.STATE_FAILED,
            'Work4': GraphRiteSession.STATE_STARTED
        }
        self.assertTrue(self.mAwaiter.keepWaiting(workStates))

if __name__ == '__main__':
    unittest.main()
