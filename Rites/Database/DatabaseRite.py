import time

import Rites.RiteCommon

from Rites.Database.DatabaseMessageProcessor import DatabaseMessageProcessor
from Rites.Rite                              import Rite

class DatabaseRite(Rite):
    def __init__(self, aCritter, aCritterData, aSettings, aPostOffice):
        Rite.__init__(self,
                      aCritter,
                      aCritterData,
                      aSettings,
                      aPostOffice,
                      Rites.RiteCommon.DATABASE,
                      DatabaseMessageProcessor)

    def run(self):
        while True:
            self.mLogger.debug("Sleeping for a heartbeat.")
            time.sleep(self.mSettings.get('heartbeat', 'period'))
