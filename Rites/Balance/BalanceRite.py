"""The balance rite."""

import time

import Rites.RiteCommon

from Rites.Balance.BalanceMessageProcessor import BalanceMessageProcessor
from Rites.Rite                            import Rite

class BalanceRite(Rite):
    """The balance rite.

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
        Rite.__init__(self,
                      aCritter,
                      aCritterData,
                      aSettings,
                      aPostOffice,
                      Rites.RiteCommon.BALANCE,
                      BalanceMessageProcessor)

    def run(self):
        """Starts the main loop of the rite."""
        while True:
            self.mLogger.debug("Sleeping for a heartbeat.")
            time.sleep(self.mSettings.get('heartbeat', 'period'))
