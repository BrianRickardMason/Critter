"""The scheduler rite."""

import time

import Rites.RiteCommon

from Rites.Rite                                import Rite
from Rites.Scheduler.SchedulerCommands         import SchedulerCommandCheckSchedule
from Rites.Scheduler.SchedulerMessageProcessor import SchedulerMessageProcessor

class SchedulerRite(Rite):
    """The scheduler rite.

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
                      Rites.RiteCommon.SCHEDULER,
                      SchedulerMessageProcessor)

    def run(self):
        """Starts the main loop of the rite."""
        while True:
            self.mLogger.debug("Checking the schedule.")
            command = SchedulerCommandCheckSchedule()
            self.mPostOffice.putCommand('Scheduler', command)

            self.mLogger.debug("Sleeping for a heartbeat.")
            time.sleep(self.mSettings.get('heartbeat', 'period'))
