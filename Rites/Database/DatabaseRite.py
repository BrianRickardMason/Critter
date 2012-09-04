import time

import Rites.RiteCommon

from Rites.Database.DatabaseMessageProcessor import DatabaseMessageProcessor
from Rites.Rite                              import Rite

class DatabaseRite(Rite):
    def __init__(self, aCritter, aCritterData, aSettings, aPostOffice):
        Rite.__init__(self,
                      aCritter,
                      aCritterData,
                      aSettings,
                      aPostOffice,
                      Rites.RiteCommon.DATABASE,
                      DatabaseMessageProcessor)

        # A dictionary of received requests.
        self.mRecvReq = {}
        self.mRecvReq['Command_DetermineGraphCycle_Req'] = {}
        self.mRecvReq['Command_DetermineWorkCycle_Req'] = {}
        self.mRecvReq['Command_LoadGraphDetails_Req'] = {}

    def run(self):
        while True:
            self.mLogger.debug("Sleeping for a heartbeat.")
            time.sleep(self.mSettings.get('heartbeat', 'period'))

    def insertRecvRequest(self, aMessageName, aCritthash, aMessage, aSoftTimeout=3, aHardTimeout=5):
        assert aCritthash not in self.mRecvReq[aMessageName], "Not handled yet. Duplicated critthash."
        self.mLogger.debug("Insert(ing) the recv request: [%s][%s]." % (aMessageName, aCritthash))
        self.mRecvReq[aMessageName][aCritthash] = {
            'message':     aMessage,
            'softTimeout': aSoftTimeout,
            'hardTimeout': aHardTimeout
        }

    def deleteRecvRequest(self, aMessageName, aCritthash):
        if aCritthash in self.mRecvReq[aMessageName]:
            self.mLogger.debug("Delete(ing) the recv request: [%s][%s]." % (aMessageName, aCritthash))
            del self.mRecvReq[aMessageName][aCritthash]
