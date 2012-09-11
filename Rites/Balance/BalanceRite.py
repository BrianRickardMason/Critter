import time

import Rites.RiteCommon

from Rites.Balance.BalanceCommands         import BalanceCommand_Auto_LoadGraphAndWork
from Rites.Balance.BalanceCommands         import BalanceCommand_Fault_HardTimeout
from Rites.Balance.BalanceCommands         import BalanceCommand_Fault_SoftTimeout
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
            self.checkTimeouts()

            self.mLogger.debug("Loading the data.")
            command = BalanceCommand_Auto_LoadGraphAndWork()
            # FIXME: Use the prioritized interface.
            self.mPostOffice.putCommand(Rites.RiteCommon.BALANCE, command)

            self.mLogger.debug("Sleeping for a heartbeat.")
            time.sleep(self.mSettings.get('heartbeat', 'period'))

    def setState(self, aState):
        self.mState = aState

    def checkTimeouts(self):
        timestamp = time.time()
        # TODO: Define what should be the order of checking?
        self.checkTimeoutsForSpecificMessages(self.mRecvReq, timestamp)
        self.checkTimeoutsForSpecificMessages(self.mSentReq, timestamp)

    def checkTimeoutsForSpecificMessages(self, aMessages, aTimestamp):
        for requestName in aMessages:
            for critthash in aMessages[requestName]:
                if aTimestamp - aMessages[requestName][critthash]['timestamp'] > \
                   aMessages[requestName][critthash]['hardTimeout']:
                    command = BalanceCommand_Fault_HardTimeout(requestName, critthash)
                    # FIXME: A magic number.
                    # TODO: Define the priorities.
                    self.putCommand(command, 50)
                elif aTimestamp - aMessages[requestName][critthash]['timestamp'] > \
                     aMessages[requestName][critthash]['softTimeout']:
                    command = BalanceCommand_Fault_SoftTimeout(requestName, critthash)
                    # FIXME: A magic number.
                    # TODO: Define the priorities.
                    self.putCommand(command, 50)
