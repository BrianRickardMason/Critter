"""The poke rite."""

import time

import Rites.RiteCommon

from Rites.Poke.PokeMessageProcessor import PokeMessageProcessor
from Rites.Rite                      import Rite

class PokeRite(Rite):
    """The poke rite.

    Attributes:
        mCommandProcessor: The command processor of the rite
        mMessageProcessor: The message processor of the rite

    """

    def __init__(self, aCritter, aCritterData, aSettings, aPostOffice):
        """Initializes the rite.

        Arguments:
            aCritter:     The critter.
            aCritterData: The critter data.
            aSettings:    The settings.
            aPostOffice:  The post office.

        """
        Rite.__init__(self, aCritter, aCritterData, aSettings, aPostOffice, Rites.RiteCommon.POKE, PokeMessageProcessor)

    def run(self):
        """Starts the main loop of the rite."""
        while True:
            self.mLogger.debug("Poking other critters.")
            envelope = self.mPostOffice.encode(
                'PokeAnnouncement',
                {'messageName': 'PokeAnnouncement',
                 'sender':      {'type': self.mCritterData.mType,
                                 'nick': self.mCritterData.mNick}})
            self.mPostOffice.putOutgoingAnnouncement(envelope)

            self.mLogger.debug("Sleeping for a heartbeat.")
            time.sleep(self.mSettings.get('heartbeat', 'period'))
