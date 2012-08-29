"""Scheduler rite commands."""

import os
import random

class SchedulerCommandCheckSchedule(object):
    def execute(self, aCommandProcessor):
        """Executes the command.

        Arguments:
            aCommandProcessor: The command processor to be visited.

        """
        # FIXME: This simulates the need of graph execution.
        if random.randint(1, 100) > 90:
            aCommandProcessor.mLogger.info("New graph execution needed.")
            # FIXME: A jealous class.
            graphNames = ['GraphName1', 'GraphName2', 'GraphName3', 'GraphName4']
            graphName = random.choice(graphNames)
            critthash = os.urandom(32).encode('hex')
            aCommandProcessor.mLogger.debug("Storing graph execution data under a hash: %s." % critthash)
            aCommandProcessor.mRite.mGraphExecutionData[critthash] = {}
            aCommandProcessor.mRite.mGraphExecutionData[critthash]['graphName'] = graphName
            aCommandProcessor.mLogger.debug("Sending the ExecuteGraphSeekVolunteers message.")
            envelope = aCommandProcessor.mRite.mPostOffice.encode(
                'ExecuteGraphSeekVolunteers',
                {'messageName': 'ExecuteGraphSeekVolunteers',
                 'sender':      {'type': aCommandProcessor.mRite.mCritterData.mType,
                                 'nick': aCommandProcessor.mRite.mCritterData.mNick},
                 'hash':        critthash})
            aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

            assert 'Command_Req_ExecuteGraph' in aCommandProcessor.mRite.mSentCommands, "Missing key in the dictionary of sent commands."

            if critthash in aCommandProcessor.mRite.mSentCommands['Command_Req_ExecuteGraph']:
                assert False, "Not handled yet. Duplicated critthash."
            else:
                aCommandProcessor.mRite.mSentCommands['Command_Req_ExecuteGraph'][critthash] = {'critthash': critthash}

            envelope = aCommandProcessor.mRite.mPostOffice.encode(
                'Command_Req_ExecuteGraph',
                {'messageName': 'Command_Req_ExecuteGraph',
                 'critthash':   critthash,
                 'graphName':   graphName}
            )
            aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

class SchedulerCommand_Handle_ExecuteGraphSeekVolunteers(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        hashValue = self.mMessage.hash
        if hashValue in aCommandProcessor.mRite.mGraphExecutionData:
            aCommandProcessor.mRite.mGraphExecutionData[hashValue]['leadingCriduler'] = self.mMessage.sender.nick
        else:
            aCommandProcessor.mLogger.warn("Hash is unavailable.")

class SchedulerCommand_Handle_ExecuteGraphVoluntee(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mCritter.mCritterData.mType != self.mMessage.receiver.type or \
           aCommandProcessor.mRite.mCritter.mCritterData.mNick != self.mMessage.receiver.nick    :
            aCommandProcessor.mLogger.debug("The message is not addressed to me.")
            return

        hashValue = self.mMessage.hash

        if not hashValue in aCommandProcessor.mRite.mGraphExecutionData:
            aCommandProcessor.mLogger.warn("Hash is unavailable.")
            return

        if 'leadingGraphYeeti' in aCommandProcessor.mRite.mGraphExecutionData[hashValue]:
            aCommandProcessor.mLogger.debug("Leading GraphYeeti has already been selected.")
            return

        aCommandProcessor.mRite.mGraphExecutionData[hashValue]['leadingGraphYeeti'] = self.mMessage.sender.nick

        aCommandProcessor.mLogger.debug("Sending the ExecuteGraphSelectVolunteer.")
        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            'ExecuteGraphSelectVolunteer',
            {'messageName': 'ExecuteGraphSelectVolunteer',
             'sender':      {'type': aCommandProcessor.mRite.mCritterData.mType,
                             'nick': aCommandProcessor.mRite.mCritterData.mNick},
             'receiver':    {'type': self.mMessage.sender.type,
                             'nick': self.mMessage.sender.nick},
             'hash':        hashValue,
             'graphName':   aCommandProcessor.mRite.mGraphExecutionData[hashValue]['graphName']})
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

class SchedulerCommand_Handle_ExecuteGraphSelectVolunteer(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mCritter.mCritterData.mNick == self.mMessage.sender.type and \
           aCommandProcessor.mRite.mCritter.mCritterData.mNick == self.mMessage.sender.type     :
            aCommandProcessor.mLogger.debug("The message is sent by me.")
            return

        hashValue = self.mMessage.hash

        aCommandProcessor.mRite.mGraphExecutionData[hashValue]['leadingGraphYeeti'] = self.mMessage.receiver.nick
