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
        # FIXME: What happens when there are not any workers?
        foundWorker = choice(availableWorkers)

        # Command work execution.
        # FIXME: Remove hardcodes.
        foundWorkerData = CritterData('Worker', foundWorker)

        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            'ExecuteWorkAnnouncement',
            {'messageName': 'ExecuteWorkAnnouncement',
             'sender':      {'type': aCommandProcessor.mRite.mCritterData.mType,
                             'nick': aCommandProcessor.mRite.mCritterData.mNick},
             'receiver':    {'type': foundWorkerData.mType,
                             'nick': foundWorkerData.mNick},
             'graphName':   self.mMessage.graphName,
             'cycle':       self.mMessage.cycle,
             'workName':    self.mMessage.workName})
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

class BalanceCommand_Handle_CommandWorkExecutionSeekVolunteers(object):
    def __init__(self, aMessage):
        self.mName = "BalanceCommand_Handle_CommandWorkExecutionSeekVolunteers"
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        hashValue = self.mMessage.hash
        if hashValue in aCommandProcessor.mRite.mCommandWorkExecutionVolunteering:
            # TODO: Handle it!
            aCommandProcessor.mLogger.error("Hash is available - conflict.")
            return

        aCommandProcessor.mLogger.debug("Storing CommandWorkExecution volunteering data under a hash: %s." % hashValue)
        aCommandProcessor.mRite.mCommandWorkExecutionVolunteering[hashValue] = {}
        aCommandProcessor.mRite.mCommandWorkExecutionVolunteering[hashValue]['boss'] = self.mMessage.sender.nick

        aCommandProcessor.mLogger.debug("Sending the CommandWorkExecutionVoluntee message.")
        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            'CommandWorkExecutionVoluntee',
            {'messageName': 'CommandWorkExecutionVoluntee',
             'sender':      {'type': aCommandProcessor.mRite.mCritterData.mType,
                             'nick': aCommandProcessor.mRite.mCritterData.mNick},
             'receiver':    {'type': self.mMessage.sender.type,
                             'nick': self.mMessage.sender.nick},
             'hash':        hashValue})
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)
