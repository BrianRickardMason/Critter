import time

import Rites.RiteCommon

from Rites.Work.WorkCommands         import WorkCommand_Auto_LoadGraphAndWork
from Rites.Work.WorkMessageProcessor import WorkMessageProcessor
from Rites.Rite                      import Rite

class WorkRite(Rite):
    def __init__(self, aCritter, aSettings, aPostOffice):
        Rite.__init__(self,
                      aCritter,
                      aSettings,
                      aPostOffice,
                      Rites.RiteCommon.BALANCE,
                      WorkMessageProcessor)

        # The state of the rite.
        self.mState = Rites.RiteCommon.STATE_STARTING

        # The dictionary of received requests.
        self.mRecvReq = {}
        self.mRecvReq['Command_ExecuteWork_Req'] = {}

        # The dictionary of sent requests.
        self.mSentReq = {}
        self.mSentReq['Command_DetermineWorkCycle_Req'] = {}
        self.mSentReq['Command_LoadGraphAndWork_Req'  ] = {}
        self.mSentReq['Command_LoadGraphDetails_Req'  ] = {}
        self.mSentReq['Command_LoadWorkDetails_Req'   ] = {}

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
            command = WorkCommand_Auto_LoadGraphAndWork()
            self.mPostOffice.putCommand(Rites.RiteCommon.WORK, command)

            self.mLogger.debug("Sleeping for a heartbeat.")
            time.sleep(self.mSettings.get('heartbeat', 'period'))

    def setState(self, aState):
        self.mState = aState
