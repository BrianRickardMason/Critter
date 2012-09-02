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
