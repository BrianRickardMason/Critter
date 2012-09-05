import os
import time

import Rites.RiteCommon

from Rites.Rite                                import Rite
from Rites.Scheduler.SchedulerCommands         import SchedulerCommand_Auto_CheckSchedule
from Rites.Scheduler.SchedulerCommands         import SchedulerCommand_Auto_LoadGraphDetails
from Rites.Scheduler.SchedulerMessageProcessor import SchedulerMessageProcessor

class SchedulerRite(Rite):
    def __init__(self, aCritter, aCritterData, aSettings, aPostOffice):
        Rite.__init__(self,
                      aCritter,
                      aCritterData,
                      aSettings,
                      aPostOffice,
                      Rites.RiteCommon.SCHEDULER,
                      SchedulerMessageProcessor)

        # The dictionary of sent commands.
        self.mSentReq = {}
        self.mSentReq['Command_ExecuteGraph_Req'] = {}
        self.mSentReq['Command_LoadGraphDetails_Req'] = {}

        # The dictionary of graph details.
        self.mGraphDetails = {}

        # The state of the rite.
        self.mState = Rites.RiteCommon.STATE_STARTING

    def run(self):
        while True:
            # TODO: Check the messages that timed out.

            self.mLogger.debug("Loading the graph details.")
            command = SchedulerCommand_Auto_LoadGraphDetails()
            self.mPostOffice.putCommand(Rites.RiteCommon.SCHEDULER, command)

            self.mLogger.debug("Checking the schedule.")
            command = SchedulerCommand_Auto_CheckSchedule()
            self.mPostOffice.putCommand(Rites.RiteCommon.SCHEDULER, command)

            self.mLogger.debug("Sleeping for a heartbeat.")
            time.sleep(self.mSettings.get('heartbeat', 'period'))

    def setState(self, aState):
        self.mState = aState

    def insertSentRequest(self, aMessageName, aCritthash, aEnvelope, aSoftTimeout=3, aHardTimeout=5):
        assert aCritthash not in self.mSentReq[aMessageName], "Not handled yet. Duplicated critthash."
        self.mLogger.debug("Insert(ing) the sent request: [%s][%s]." % (aMessageName, aCritthash))
        self.mSentReq[aMessageName][aCritthash] = {
            'envelope':    aEnvelope,
            'softTimeout': aSoftTimeout,
            'hardTimeout': aHardTimeout
        }
        self.mLogger.debug("Sending the %s message." % aMessageName)
        self.mPostOffice.putOutgoingAnnouncement(aEnvelope)

    def deleteSentRequest(self, aMessageName, aCritthash):
        if aCritthash in self.mSentReq[aMessageName]:
            self.mLogger.debug("Delete(ing) the sent request: [%s][%s]." % (aMessageName, aCritthash))
            del self.mSentReq[aMessageName][aCritthash]
