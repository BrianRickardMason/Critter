import copy
import time

import Rites.RiteCommon

from Critter.PostOffice.SubscriptionChannels import SUBSCRIPTION_CHANNEL_ALL
from Rites.Registry.RegistryCommands         import RegistryCommand_Auto_CheckHeartbeats
from Rites.Registry.RegistryMessageProcessor import RegistryMessageProcessor
from Rites.Rite                              import Rite

class RegistryRite(Rite):
    def __init__(self, aCritter, aSettings, aPostOffice):
        self.mSettings = aSettings

        Rite.__init__(self,
                      aCritter,
                      aSettings,
                      aPostOffice,
                      Rites.RiteCommon.REGISTRY,
                      RegistryMessageProcessor)

        # Set subscription channels.
        self.mPostOffice.addSubscriptionChannel(SUBSCRIPTION_CHANNEL_ALL)

        # The dictionary of received requests.
        self.mRecvReq = {}
        self.mRecvReq['Command_PresentYourself_Req'] = {}

        # The dictionary of sent requests.
        self.mSentReq = {}
        self.mSentReq['Command_PresentYourself_Req'] = {}

        # The dictionary of known crittnicks.
        self.mKnownCrittnicks = {}

        # The dictionary of known heartbeats.
        self.mKnownHeartbeats = {}

        # The dictionary of known rites.
        self.mKnownRites = {}

    def run(self):
        while True:
            self.mLogger.debug("Checking the heartbeats.")
            command = RegistryCommand_Auto_CheckHeartbeats()
            self.mPostOffice.putCommand(Rites.RiteCommon.REGISTRY, command)

            self.mLogger.debug("Sleeping for a heartbeat.")
            time.sleep(self.mSettings.get('heartbeat', 'period'))

    def getKnownCritters(self):
        return (
            copy.deepcopy(self.mKnownCrittnicks),
            copy.deepcopy(self.mKnownHeartbeats),
            copy.deepcopy(self.mKnownRites)
        )

    def getNumberOfKnownCritters(self):
        return len(self.mKnownCrittnicks)
