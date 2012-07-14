"""The registry rite."""

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

    def __init__(self, aCritterData, aSettings, aPostOffice):
        """Initializes the rite.

        Arguments:
            aCritterData: The critter data.
            aSettings:    The settings.
            aPostOffice:  The post office.

        """
        self.mSettings = aSettings

        self.mKnownCritters           = {}
        self.mKnownCrittersHeartbeats = {}

        Rite.__init__(self, aCritterData, aSettings, aPostOffice, Rites.RiteCommon.REGISTRY, RegistryMessageProcessor)

    def run(self):
        """Starts the main loop of the rite."""
        while True:
            self.mLogger.debug("Checking the heartbeats.")
            command = RegistryCommandCheckHeartbeats()
            self.mPostOffice.putCommand('Registry', command)

            self.mLogger.debug("Sleeping for a heartbeat.")
            time.sleep(self.mSettings.get('heartbeat', 'period'))

    def getNumberOfKnownCritters(self):
        """Returns the number of known critters.

        Returns The number of known critters.

        """
        return len(self.mKnownCritters)
