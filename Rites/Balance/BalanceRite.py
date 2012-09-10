import time

import Rites.RiteCommon

from Rites.Balance.BalanceCommands         import BalanceCommand_Auto_LoadGraphAndWork
from Rites.Balance.BalanceMessageProcessor import BalanceMessageProcessor
from Rites.Rite                            import Rite

class BalanceRite(Rite):
    def __init__(self, aCritter, aSettings, aPostOffice):
        Rite.__init__(self,
                      aCritter,
                      aSettings,
                      aPostOffice,
                      Rites.RiteCommon.BALANCE,
                      BalanceMessageProcessor)

        # The state of the rite.
        self.mState = Rites.RiteCommon.STATE_STARTING

        # The dictionary of received requests.
        self.mRecvReq = {}
        self.mRecvReq['Command_OrderWorkExecution_Req'] = {}

        # The dictionary of sent requests.
        self.mSentReq = {}
        self.mSentReq['Command_Election_Req'        ] = {}
        self.mSentReq['Command_ExecuteWork_Req'     ] = {}
        self.mSentReq['Command_LoadGraphAndWork_Req'] = {}
        self.mSentReq['Command_LoadGraphDetails_Req'] = {}
        self.mSentReq['Command_LoadWorkDetails_Req' ] = {}

        # The dictionary of elections.
        self.mElections = {}

        # Dictionaries of graph data.
        self.mGraphs       = []
        self.mGraphDetails = {}

        # Dictionaries of work data.
        self.mWorks            = {}
        self.mWorkDetails      = {}
        self.mWorkPredecessors = {}

    def run(self):
        while True:
            # TODO: Check the messages that timed out.

            self.mLogger.debug("Loading the data.")
            command = BalanceCommand_Auto_LoadGraphAndWork()
            self.mPostOffice.putCommand(Rites.RiteCommon.BALANCE, command)

            self.mLogger.debug("Sleeping for a heartbeat.")
            time.sleep(self.mSettings.get('heartbeat', 'period'))

    def setState(self, aState):
        self.mState = aState
