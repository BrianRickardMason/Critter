import os
import random

class SchedulerCommandCheckSchedule(object):
    def execute(self, aCommandProcessor):
        # FIXME: This simulates the need of graph execution.
        if random.randint(1, 100) > 50:
            aCommandProcessor.mLogger.info("New graph execution needed.")

            graphNames = ['GraphName1', 'GraphName2', 'GraphName3', 'GraphName4']

            critthash = os.urandom(32).encode('hex')

            assert 'Command_Req_ExecuteGraph' in aCommandProcessor.mRite.mSentCommands, "Missing key in the dictionary of sent commands."
            assert critthash not in aCommandProcessor.mRite.mSentCommands['Command_Req_ExecuteGraph'], "Not handled yet. Duplicated critthash."

            aCommandProcessor.mLogger.debug("Storing the sent message entry: [%s][%s]." % ('Command_Req_ExecuteGraph', critthash))
            aCommandProcessor.mRite.mSentCommands['Command_Req_ExecuteGraph'][critthash] = {'critthash': critthash}

            aCommandProcessor.mLogger.debug("Sending the Command_Req_ExecuteGraph message.")
            envelope = aCommandProcessor.mRite.mPostOffice.encode(
                'Command_Req_ExecuteGraph',
                {'messageName': 'Command_Req_ExecuteGraph',
                 'critthash':   critthash,
                 'graphName':   random.choice(graphNames)}
            )
            aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)
