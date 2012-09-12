"""The registry rite."""

import copy
import time

import Rites.RiteCommon

from Rites.Registry.RegistryCommands         import RegistryCommandCheckHeartbeats
from Rites.Registry.RegistryMessageProcessor import RegistryMessageProcessor
from Rites.Rite                              import Rite

class RegistryRite(Rite):
    """The registry rite.

    Attributes:
        mCommandProcessor: The command processor of the rite
        mMessageProcessor: The message processor of the rite

    """

    def __init__(self, aCritter, aSettings, aPostOffice):
        """Initializes the rite.

        Arguments:
            aCritter:    The critter.
            aSettings:   The settings.
            aPostOffice: The post office.

        """
        self.mSettings = aSettings

        Rite.__init__(self,
                      aCritter,
                      aSettings,
                      aPostOffice,
                      Rites.RiteCommon.REGISTRY,
                      RegistryMessageProcessor)


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
        """Starts the main loop of the rite."""
        while True:
            self.mLogger.debug("Checking the heartbeats.")
            command = RegistryCommandCheckHeartbeats()
            self.mPostOffice.putCommand(Rites.RiteCommon.REGISTRY, command)

            self.mLogger.debug("Sleeping for a heartbeat.")
            time.sleep(self.mSettings.get('heartbeat', 'period'))

    def getKnownCritters(self):
        """Returns the dictionary of known critters.

        Returns:
            The copy of the dictionary of known critters.
        """
        return (
            copy.deepcopy(self.mKnownCrittnicks),
            copy.deepcopy(self.mKnownHeartbeats),
            copy.deepcopy(self.mKnownRites)
        )

    def getNumberOfKnownCritters(self):
        """Returns the number of known critters.

        Returns The number of known critters.

        """
        return len(self.mKnownCrittnicks)
