import time

import Rites.RiteCommon

from Rites.Poke.PokeMessageProcessor import PokeMessageProcessor
from Rites.Rite                      import Rite

class PokeRite(Rite):
    def __init__(self, aCritter, aCritterData, aSettings, aPostOffice):
        Rite.__init__(self, aCritter, aCritterData, aSettings, aPostOffice, Rites.RiteCommon.POKE, PokeMessageProcessor)

    def run(self):
        while True:
            self.mLogger.debug("Poking other critters.")
            messageName = 'Announcement_Poke'
            envelope = self.mPostOffice.encode(
                messageName,
                {'messageName': messageName,
                 'crittnick':   self.mCritter.mCritterData.mNick}
            )
            self.mPostOffice.putOutgoingAnnouncement(envelope)

            self.mLogger.debug("Sleeping for a heartbeat.")
            time.sleep(self.mSettings.get('heartbeat', 'period'))
