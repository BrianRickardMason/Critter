"""Balance rite commands."""

from random import choice

import Rites.RiteCommon

from Critter.CritterData import CritterData

class BalanceCommandCommandWorkExecution(object):
    """CommandWorkExecution command.

    Attributes:
        mName:    The name of the command.
        mMessage: The CommandWorkExecutionAnnouncement.

    """

    def __init__(self, aMessage):
        """Initializes the command.

        Arguments:
            aMessage: The CommandWorkExecutionAnnouncement.

        """
        self.mName    = 'CommandWorkExecution'
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        """Executes the command.

        Arguments:
            aCommandProcessor: The command processor to be visited.

        """
        # Get the list of known critters.
        # FIXME: Jealous class.
        knownCritters = aCommandProcessor.mRite.mCritter.mRites[Rites.RiteCommon.REGISTRY].getKnownCritters()

        # Filter workers.
        availableWorkers = []
        for critterData in knownCritters.values():
            if critterData.mType == 'Worker':
                availableWorkers.append(critterData.mNick)

        # Balance the load.
        foundWorker = choice(availableWorkers)

        # Command work execution.
        # FIXME: Remove hardcodes.
        foundWorkerData = CritterData('Worker', foundWorker)

        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            'ExecuteWorkAnnouncement',
            {'sender':    aCommandProcessor.mRite.mCritterData,
             'receiver':  foundWorkerData,
             'graphName': self.mMessage.graphName,
             'cycle':     self.mMessage.cycle,
             'workName':  self.mMessage.workName})
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)
