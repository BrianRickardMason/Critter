import time

import Rites.RiteCommon

from Critter.PostOffice.SubscriptionChannels import SUBSCRIPTION_CHANNEL_ALL
from Rites.Database.DatabaseMessageProcessor import DatabaseMessageProcessor
from Rites.Rite                              import Rite

class DatabaseRite(Rite):
    def __init__(self, aCritter, aSettings, aPostOffice):
        Rite.__init__(self,
                      aCritter,
                      aSettings,
                      aPostOffice,
                      Rites.RiteCommon.DATABASE,
                      DatabaseMessageProcessor)

        # Set subscription channels.
        self.mPostOffice.addSubscriptionChannel(SUBSCRIPTION_CHANNEL_ALL)

        # The dictionary of received requests.
        # TODO: Add perl's auto-vivification.
        self.mRecvReq = {}
        self.mRecvReq['Command_DescribeCrittwork_Req'  ] = {}
        self.mRecvReq['Command_DetermineGraphCycle_Req'] = {}
        self.mRecvReq['Command_DetermineWorkCycle_Req' ] = {}
        self.mRecvReq['Command_LoadGraphAndWork_Req'   ] = {}
        self.mRecvReq['Command_LoadGraphDetails_Req'   ] = {}
        self.mRecvReq['Command_LoadWorkDetails_Req'    ] = {}

    def run(self):
        while True:
            self.mLogger.debug("Sleeping for a heartbeat.")
            time.sleep(self.mSettings.get('heartbeat', 'period'))
