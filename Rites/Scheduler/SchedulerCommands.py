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
            graphName = random.choice(graphNames)
            envelope = aCommandProcessor.mRite.mPostOffice.encode(
                'ExecuteGraphAnnouncement',
                {'messageName': 'ExecuteGraphAnnouncement',
                 'sender':      {'type': aCommandProcessor.mRite.mCritterData.mType,
                                 'nick': aCommandProcessor.mRite.mCritterData.mNick},
                 'graphName':   graphName})
            aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

            # Voluntees.
            hash = os.urandom(32).encode('hex')
            aCommandProcessor.mLogger.debug("Storing graph execution data under hash: %s." % hash)
            aCommandProcessor.mRite.mGraphExecutionData[hash] = {}
            aCommandProcessor.mRite.mGraphExecutionData[hash]['graphName'] = graphName
            aCommandProcessor.mLogger.debug("Sending the ExecuteGraphSeekVolunteers message.")
            envelope = aCommandProcessor.mRite.mPostOffice.encode(
                'ExecuteGraphSeekVolunteers',
                {'messageName': 'ExecuteGraphSeekVolunteers',
                 'sender':      {'type': aCommandProcessor.mRite.mCritterData.mType,
                                 'nick': aCommandProcessor.mRite.mCritterData.mNick},
                 'hash':        hash})
            aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

class SchedulerCommand_Handle_ExecuteGraphSeekVolunteers(object):
    def __init__(self, aMessage):
        self.mName = "SchedulerCommand_Handle_ExecuteGraphSeekVolunteers"
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        hash = self.mMessage.hash
        if hash in aCommandProcessor.mRite.mGraphExecutionData:
            aCommandProcessor.mRite.mGraphExecutionData[hash]['leadingCriduler'] = self.mMessage.sender.nick
        else:
            aCommandProcessor.mLogger.warn("Hash is unavailable.")

class SchedulerCommand_Handle_ExecuteGraphVoluntee(object):
    def __init__(self, aMessage):
        self.mName = "SchedulerCommand_Handle_ExecuteGraphVoluntee"
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mCritter.mCritterData.mType != self.mMessage.receiver.type or \
           aCommandProcessor.mRite.mCritter.mCritterData.mNick != self.mMessage.receiver.nick    :
            aCommandProcessor.mLogger.debug("The message is not addressed to me.")
            return

        hash = self.mMessage.hash

        if not hash in aCommandProcessor.mRite.mGraphExecutionData:
            aCommandProcessor.mLogger.warn("Hash is unavailable.")
            return

        if 'leadingGraphYeeti' in aCommandProcessor.mRite.mGraphExecutionData[hash]:
            aCommandProcessor.mLogger.debug("Leading GraphYeeti has already been selected.")
            return

        aCommandProcessor.mRite.mGraphExecutionData[hash]['leadingGraphYeeti'] = self.mMessage.sender.nick

        aCommandProcessor.mLogger.debug("Sending the ExecuteGraphSelectVolunteer.")
        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            'ExecuteGraphSelectVolunteer',
            {'messageName': 'ExecuteGraphSelectVolunteer',
             'sender':      {'type': aCommandProcessor.mRite.mCritterData.mType,
                             'nick': aCommandProcessor.mRite.mCritterData.mNick},
             'receiver':    {'type': self.mMessage.sender.type,
                             'nick': self.mMessage.sender.nick},
             'hash':        hash,
             'graphName':   aCommandProcessor.mRite.mGraphExecutionData[hash]['graphName']})
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

class SchedulerCommand_Handle_ExecuteGraphSelectVolunteer(object):
    def __init__(self, aMessage):
        self.mName = "SchedulerCommand_Handle_ExecuteGraphSelectVolunteer"
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mCritter.mCritterData.mNick == self.mMessage.sender.type and \
           aCommandProcessor.mRite.mCritter.mCritterData.mNick == self.mMessage.sender.type     :
            aCommandProcessor.mLogger.debug("The message is sent by me.")
            return

        aCommandProcessor.mRite.mGraphExecutionData[hash]['leadingGraphYeeti'] = self.mMessage.receiver.nick
