"""Unit tests."""

import unittest

from GraphRiteSession import SpawnChecker

class SpawnChecker_ContinueSpawning(unittest.TestCase):

    def setUp(self):
        self.mSpawnChecker = SpawnChecker()

    def testContinueSpawningReturnsTrueIfThereIsOnlyOneNotStartedState(self):
        workStates = \
        {
            'Work1': 0
        }
        self.assertTrue(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsFalseIfThereIsOnlyOneStartedState(self):
        workStates = \
        {
            'Work1': 1
        }
        self.assertFalse(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsFalseIfThereIsOnlyOneSucceedState(self):
        workStates = \
        {
            'Work1': 2
        }
        self.assertFalse(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsFalseIfThereIsOnlyOneFailedState(self):
        workStates = \
        {
            'Work1': 3
        }
        self.assertFalse(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsTrueIfThereAreOnlyNotStartedStates(self):
        workStates = \
        {
            'Work1': 0,
            'Work2': 0,
            'Work3': 0,
            'Work4': 0
        }
        self.assertTrue(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsFalseIfThereAreOnlyStartedStates(self):
        workStates = \
        {
            'Work1': 1,
            'Work2': 1,
            'Work3': 1,
            'Work4': 1
        }
        self.assertFalse(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsFalseIfThereAreOnlySucceedStates(self):
        workStates = \
        {
            'Work1': 2,
            'Work2': 2,
            'Work3': 2,
            'Work4': 2
        }
        self.assertFalse(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsFalseIfThereAreOnlyFailedStates(self):
        workStates = \
        {
            'Work1': 3,
            'Work2': 3,
            'Work3': 3,
            'Work4': 3
        }
        self.assertFalse(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsTrueIfThereAreOnlyNotStartedAndStartedStates_OneNotStartedOneStarted(self):
        workStates = \
        {
            'Work1': 0,
            'Work2': 1
        }
        self.assertTrue(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsTrueIfThereAreOnlyNotStartedAndStartedStates_ManyNotStartedOneStarted(self):
        workStates = \
        {
            'Work1': 0,
            'Work2': 0,
            'Work3': 1,
            'Work4': 0
        }
        self.assertTrue(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsTrueIfThereAreOnlyNotStartedAndStartedStates_OneNotStartedManyStarted(self):
        workStates = \
        {
            'Work1': 1,
            'Work2': 1,
            'Work3': 0,
            'Work4': 1
        }
        self.assertTrue(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsTrueIfThereAreOnlyNotStartedAndSucceedStates_OneNotStartedOneSucceed(self):
        workStates = \
        {
            'Work1': 0,
            'Work2': 2
        }
        self.assertTrue(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsTrueIfThereAreOnlyNotStartedAndSucceedStates_ManyNotStartedOneSucceed(self):
        workStates = \
        {
            'Work1': 0,
            'Work2': 0,
            'Work3': 2,
            'Work4': 0
        }
        self.assertTrue(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsTrueIfThereAreOnlyNotStartedAndSucceedStates_OneNotStartedManySucceed(self):
        workStates = \
        {
            'Work1': 2,
            'Work2': 2,
            'Work3': 0,
            'Work4': 2
        }
        self.assertTrue(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsTrueIfThereAreOnlyOneNotStartedAndStartedAndSucceedStates_OneNotStartedManyStartedManySuceed(self):
        workStates = \
        {
            'Work1': 1,
            'Work2': 2,
            'Work3': 1,
            'Work4': 2,
            'Work5': 0
        }
        self.assertTrue(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsFalseIfThereAreOnlyStartedAndSucceedStates_OneStartedOneSucceed(self):
        workStates = \
        {
            'Work1': 1,
            'Work2': 2
        }
        self.assertFalse(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsFalseIfThereAreOnlyStartedAndSucceedStates_ManyStartedManySucceed(self):
        workStates = \
        {
            'Work1': 1,
            'Work2': 2,
            'Work3': 1,
            'Work4': 2,
            'Work5': 1
        }
        self.assertFalse(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsFalseIfThereIsAFailedState(self):
        workStates = \
        {
            'Work1': 0,
            'Work2': 3
        }
        self.assertFalse(self.mSpawnChecker.continueSpawning(workStates))

    def testContinueSpawningReturnsFalseIfThereAreOnlyStartedAndFailedStates(self):
        workStates = \
        {
            'Work1': 1,
            'Work2': 3,
            'Work3': 1
        }
        self.assertFalse(self.mSpawnChecker.continueSpawning(workStates))

if __name__ == '__main__':
    unittest.main()
