"""The heartbeat rite."""

import time

import Rites.RiteCommon

from Rites.Heartbeat.HeartbeatMessageProcessor import HeartbeatMessageProcessor
from Rites.Rite                                import Rite

class HeartbeatRite(Rite):
    """The heartbeat rite.

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
        Rite.__init__(self, aCritterData, aSettings, aPostOffice, Rites.RiteCommon.HEARTBEAT, HeartbeatMessageProcessor)

    def run(self):
        """Starts the main loop of the rite."""
        while True:
            self.mLogger.debug("My heart beats.")
            envelope = self.mPostOffice.encode("HeartbeatAnnouncement",
                                               {'critterData': self.mCritterData,
                                                'timestamp': time.time()})
            self.mPostOffice.putOutgoingAnnouncement(envelope)

            self.mLogger.debug("Sleeping for a heartbeat.")
            time.sleep(self.mSettings.get('heartbeat', 'period'))
