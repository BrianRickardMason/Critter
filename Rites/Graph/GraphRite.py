import time

import Rites.RiteCommon

from Rites.Graph.GraphCommands         import GraphCommand_Auto_LoadGraphAndWork
from Rites.Graph.GraphMessageProcessor import GraphMessageProcessor
from Rites.Rite                        import Rite

class GraphRite(Rite):
    def __init__(self, aCritter, aSettings, aPostOffice):
        Rite.__init__(self,
                      aCritter,
                      aSettings,
                      aPostOffice,
                      Rites.RiteCommon.GRAPH,
                      GraphMessageProcessor)

        # The state of the rite.
        self.mState = Rites.RiteCommon.STATE_STARTING

        # The dictionary of received requests.
        self.mRecvReq = {}
        self.mRecvReq['Command_ExecuteGraph_Req'] = {}

        # The dictionary of sent requests.
        self.mSentReq = {}
        self.mSentReq['Command_DetermineGraphCycle_Req'] = {}
        self.mSentReq['Command_Election_Req'           ] = {}
        self.mSentReq['Command_LoadGraphAndWork_Req'   ] = {}
        self.mSentReq['Command_LoadGraphDetails_Req'   ] = {}
        self.mSentReq['Command_LoadWorkDetails_Req'    ] = {}
        self.mSentReq['Command_OrderWorkExecution_Req' ] = {}

        # The dictionary of elections.
        self.mElections = {}

        # Dictionaries of graph data.
        self.mGraphs       = []
        self.mGraphDetails = {}

        # Dictionaries of work data.
        self.mWorks            = {}
        self.mWorkDetails      = {}
        self.mWorkPredecessors = {}

        # The dictionary of sessions.
        self.mSessions = {}

    def run(self):
        while True:
            # TODO: Check the messages that timed out.

            self.mLogger.debug("Loading the data.")
            command = GraphCommand_Auto_LoadGraphAndWork()
            self.mPostOffice.putCommand(Rites.RiteCommon.GRAPH, command)

            # TODO: Remove me. For debug purposes only.
            if 'GraphName1' in self.mSessions:
                self.mLogger.debug("The number of sessions GraphName1: %d" % len(self.mSessions['GraphName1']))
            if 'GraphName2' in self.mSessions:
                self.mLogger.debug("The number of sessions GraphName2: %d" % len(self.mSessions['GraphName2']))
            if 'GraphName3' in self.mSessions:
                self.mLogger.debug("The number of sessions GraphName3: %d" % len(self.mSessions['GraphName3']))
            if 'GraphName4' in self.mSessions:
                self.mLogger.debug("The number of sessions GraphName4: %d" % len(self.mSessions['GraphName4']))

            self.mLogger.debug("Sleeping for a heartbeat.")
            time.sleep(self.mSettings.get('heartbeat', 'period'))

    def setState(self, aState):
        self.mState = aState

    def insertRecvRequest(self, aMessageName, aCritthash, aMessage, aSoftTimeout=3, aHardTimeout=5):
        assert aCritthash not in self.mRecvReq[aMessageName], "Not handled yet. Duplicated critthash."
        self.mLogger.debug("Insert(ing) the recv request: [%s][%s]." % (aMessageName, aCritthash))
        self.mRecvReq[aMessageName][aCritthash] = aMessage

    def deleteRecvRequest(self, aMessageName, aCritthash):
        if aCritthash in self.mRecvReq[aMessageName]:
            self.mLogger.debug("Delete(ing) the recv request: [%s][%s]." % (aMessageName, aCritthash))
            del self.mRecvReq[aMessageName][aCritthash]

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
