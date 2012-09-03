import time

import Rites.RiteCommon

from Rites.Graph.GraphMessageProcessor import GraphMessageProcessor
from Rites.Rite                        import Rite

class GraphRite(Rite):
    def __init__(self, aCritter, aCritterData, aSettings, aPostOffice):
        Rite.__init__(self,
                      aCritter,
                      aCritterData,
                      aSettings,
                      aPostOffice,
                      Rites.RiteCommon.GRAPH,
                      GraphMessageProcessor)

        self.mGraphs           = []
        self.mWorks            = {}
        self.mWorkPredecessors = {}

        self.mSessions = {}

        # A dictionary of elections.
        self.mElections = {}

        # A dictionary of received requests.
        self.mRecvReq = {}
        self.mRecvReq['Command_ExecuteGraph_Req'] = {}

        # A dictionary of sent requests.
        self.mSentReq = {}
        self.mSentReq['Command_DetermineGraphCycle_Req'] = {}
        self.mSentReq['Command_Election_Req'] = {}
        self.mSentReq['Command_OrderWorkExecution_Req'] = {}

    def run(self):
        # Ask for the configuration of graphs and works.
        envelope = self.mPostOffice.encode(
            'LoadGraphAndWorkRequest',
            {'messageName': 'LoadGraphAndWorkRequest',
             'sender':      {'type': self.mCritterData.mType,
                             'nick': self.mCritterData.mNick}})
        self.mPostOffice.putOutgoingAnnouncement(envelope)

        while True:
            self.mLogger.debug("Sleeping for a heartbeat.")

            # TODO: Remove me. For debug purposes only.
            if 'GraphName1' in self.mSessions:
                self.mLogger.debug("The number of sessions GraphName1: %d" % len(self.mSessions['GraphName1']))
            if 'GraphName2' in self.mSessions:
                self.mLogger.debug("The number of sessions GraphName2: %d" % len(self.mSessions['GraphName2']))
            if 'GraphName3' in self.mSessions:
                self.mLogger.debug("The number of sessions GraphName3: %d" % len(self.mSessions['GraphName3']))
            if 'GraphName4' in self.mSessions:
                self.mLogger.debug("The number of sessions GraphName4: %d" % len(self.mSessions['GraphName4']))

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
