import time

import Rites.RiteCommon

from Rites.Rite                                import Rite
from Rites.Scheduler.SchedulerCommands         import SchedulerCommandCheckSchedule
from Rites.Scheduler.SchedulerMessageProcessor import SchedulerMessageProcessor

class SchedulerRite(Rite):
    def __init__(self, aCritter, aCritterData, aSettings, aPostOffice):
        Rite.__init__(self,
                      aCritter,
                      aCritterData,
                      aSettings,
                      aPostOffice,
                      Rites.RiteCommon.SCHEDULER,
                      SchedulerMessageProcessor)

        # A dictionary of sent commands.
        self.mSentCommands = {}
        self.mSentCommands['Command_ExecuteGraph_Req'] = {}

    def run(self):
        while True:
            self.mLogger.debug("Checking the schedule.")
            command = SchedulerCommandCheckSchedule()
            self.mPostOffice.putCommand('Scheduler', command)

            self.mLogger.debug("Sleeping for a heartbeat.")
            time.sleep(self.mSettings.get('heartbeat', 'period'))
