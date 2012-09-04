import os
import time

import Rites.RiteCommon

from Rites.Rite                                import Rite
from Rites.Scheduler.SchedulerCommands         import SchedulerCommandCheckSchedule
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

        # A dictionary of sent commands.
        self.mSentReq = {}
        self.mSentReq['Command_ExecuteGraph_Req'] = {}
        self.mSentReq['Command_LoadGraphDetails_Req'] = {}

    def run(self):
        messageName = 'Command_LoadGraphDetails_Req'
        softTimeout = 3 # [s].
        hardTimeout = 5 # [s].
        critthash = os.urandom(32).encode('hex')
        envelope = self.mPostOffice.encode(
            messageName,
            {'messageName': messageName,
             'softTimeout': softTimeout,
             'hardTimeout': hardTimeout,
             'critthash':   critthash}
        )
        self.insertSentRequest(messageName, critthash, envelope, softTimeout, hardTimeout)

        while True:
            self.mLogger.debug("Checking the schedule.")
            command = SchedulerCommandCheckSchedule()
            self.mPostOffice.putCommand('Scheduler', command)

            self.mLogger.debug("Sleeping for a heartbeat.")
            time.sleep(self.mSettings.get('heartbeat', 'period'))

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
