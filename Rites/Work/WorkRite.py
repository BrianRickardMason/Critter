import time

import Rites.RiteCommon

from Rites.Work.WorkMessageProcessor import WorkMessageProcessor
from Rites.Rite                      import Rite

class WorkRite(Rite):
    def __init__(self, aCritter, aCritterData, aSettings, aPostOffice):
        Rite.__init__(self,
                      aCritter,
                      aCritterData,
                      aSettings,
                      aPostOffice,
                      Rites.RiteCommon.BALANCE,
                      WorkMessageProcessor)

        # A dictionary of received requests.
        self.mRecvReq = {}
        self.mRecvReq['Command_ExecuteWork_Req'] = {}

        # A dictionary of sent requests.
        self.mSentReq = {}
        self.mSentReq['Command_DetermineWorkCycle_Req'] = {}

        self.mWorkDetails = {}

        self.mSessions = {}

    def run(self):
        # Request the load of the work details.
        envelope = self.mPostOffice.encode(
            'LoadWorkDetailsRequest',
            {'messageName': 'LoadWorkDetailsRequest',
             'sender':      {'type': self.mCritterData.mType,
                             'nick': self.mCritterData.mNick}})
        self.mPostOffice.putOutgoingAnnouncement(envelope)

        while True:
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

    def insertRecvRequest(self, aMessageName, aCritthash, aMessage, aSoftTimeout=3, aHardTimeout=5):
        assert aCritthash not in self.mRecvReq[aMessageName], "Not handled yet. Duplicated critthash."
        self.mLogger.debug("Insert(ing) the recv request: [%s][%s]." % (aMessageName, aCritthash))
        self.mRecvReq[aMessageName][aCritthash] = aMessage

    def deleteRecvRequest(self, aMessageName, aCritthash):
        if aCritthash in self.mRecvReq[aMessageName]:
            self.mLogger.debug("Delete(ing) the recv request: [%s][%s]." % (aMessageName, aCritthash))
            del self.mRecvReq[aMessageName][aCritthash]
