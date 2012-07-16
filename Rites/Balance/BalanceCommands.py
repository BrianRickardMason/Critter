"""Balance rite commands."""

from random import choice

import Rites.RiteCommon

class BalanceCommandCommandWorkExecution(object):
    """CommandWorkExecution command.

    Attributes:
        mName:    The name of the command.
        mMessage: The CommandWorkExecution.

    """

    def __init__(self, aMessage):
        """Initializes the command.

        Arguments:
            aMessage: The PresentYourselfRequest.

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
        # TODO.
