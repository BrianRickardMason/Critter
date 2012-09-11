import time

import Rites.RiteCommon

from Rites.Poke.PokeMessageProcessor import PokeMessageProcessor
from Rites.Rite                      import Rite

class PokeRite(Rite):
    def __init__(self, aCritter, aSettings, aPostOffice):
        Rite.__init__(self, aCritter, aSettings, aPostOffice, Rites.RiteCommon.POKE, PokeMessageProcessor)

    def run(self):
        while True:
            self.mLogger.debug("Poking other critters.")
            messageName = 'Announcement_Poke'
            message = self.mPostOffice.encode(
                {'messageName': messageName,
                 'crittnick':   self.mCritter.mCrittnick}
            )
            self.mPostOffice.putOutgoingAnnouncement(message)

            self.mLogger.debug("Sleeping for a heartbeat.")
            time.sleep(self.mSettings.get('heartbeat', 'period'))
