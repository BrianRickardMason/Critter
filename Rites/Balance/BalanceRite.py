import time

import Rites.RiteCommon

from Rites.Balance.BalanceMessageProcessor import BalanceMessageProcessor
from Rites.Rite                            import Rite

# TODO: A generic mechanism to store sent and received messages (the information about them)!

class BalanceRite(Rite):
    def __init__(self, aCritter, aCritterData, aSettings, aPostOffice):
        Rite.__init__(self,
                      aCritter,
                      aCritterData,
                      aSettings,
                      aPostOffice,
                      Rites.RiteCommon.BALANCE,
                      BalanceMessageProcessor)

        # A dictionary of elections.
        self.mElections = {}

        # A dictionary of received requests.
        self.mRecvReq = {}
        self.mRecvReq['Command_OrderWorkExecution_Req'] = {}

        # A dictionary of sent requests.
        self.mSentReq = {}
        self.mSentReq['Command_Election_Req'] = {}
        self.mSentReq['Command_ExecuteWork_Req'] = {}

    def run(self):
        while True:
            self.mLogger.debug("Sleeping for a heartbeat.")
            time.sleep(self.mSettings.get('heartbeat', 'period'))

    def insertSentRequest(self, aMessageName, aCritthash, aEnvelope, aSoftTimeout=3, aHardTimeout=5):
        assert aCritthash not in self.mSentReq[aMessageName], "Not handled yet. Duplicated critthash."
        self.mLogger.info("Insert(ing) the sent request: [%s][%s]." % (aMessageName, aCritthash))
        self.mSentReq[aMessageName][aCritthash] = {
            'envelope':    aEnvelope,
            'softTimeout': aSoftTimeout,
            'hardTimeout': aHardTimeout
        }
        self.mLogger.info("Sending the %s message." % aMessageName)
        self.mPostOffice.putOutgoingAnnouncement(aEnvelope)

    def deleteSentRequest(self, aMessageName, aCritthash):
        if aCritthash in self.mSentReq[aMessageName]:
            self.mLogger.info("Delete(ing) the sent request: [%s][%s]." % (aMessageName, aCritthash))
            del self.mSentReq[aMessageName][aCritthash]
