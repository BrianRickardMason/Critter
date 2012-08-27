"""Scheduler rite commands."""

import os
import random

class SchedulerCommandCheckSchedule(object):
    """CheckSchedule command.

    Attributes:
        mName: The name of the command.

    """

    def __init__(self):
        """Initializes the command."""
        self.mName = "SchedulerCommandCheckSchedule"

    def execute(self, aCommandProcessor):
        """Executes the command.

        Arguments:
            aCommandProcessor: The command processor to be visited.

        """
        # FIXME: This simulates the need of graph execution.
        if random.randint(1, 100) > 90:
            aCommandProcessor.mLogger.info("New graph execution needed.")
            aCommandProcessor.mLogger.debug("Sending the ExecuteGraphAnnouncement.")
            # FIXME: A jealous class.
            graphNames = ['GraphName1', 'GraphName2', 'GraphName3', 'GraphName4']
            envelope = aCommandProcessor.mRite.mPostOffice.encode(
                'ExecuteGraphAnnouncement',
                {'messageName': 'ExecuteGraphAnnouncement',
                 'sender':      {'type': aCommandProcessor.mRite.mCritterData.mType,
                                 'nick': aCommandProcessor.mRite.mCritterData.mNick},
                 'graphName':   random.choice(graphNames)})
            aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

            # Voluntees.
            hash = os.urandom(32).encode('hex')
            aCommandProcessor.mLogger.debug("Hash value: %s." % hash)
            aCommandProcessor.mLogger.debug("Sending the ExecuteGraphSeekVolunteers.")
            envelope = aCommandProcessor.mRite.mPostOffice.encode(
                'ExecuteGraphSeekVolunteers',
                {'messageName': 'ExecuteGraphSeekVolunteers',
                 'sender':      {'type': aCommandProcessor.mRite.mCritterData.mType,
                                 'nick': aCommandProcessor.mRite.mCritterData.mNick},
                 'hash':        hash})
            aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)
