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

    def __init__(self, aCritter, aCritterData, aSettings, aPostOffice):
        """Initializes the rite.

        Arguments:
            aCritter:     The critter.
            aCritterData: The critter data.
            aSettings:    The settings.
            aPostOffice:  The post office.

        """
        self.mSettings = aSettings

        Rite.__init__(self,
                      aCritter,
                      aCritterData,
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
            self.mPostOffice.putCommand('Registry', command)

            self.mLogger.debug("Sleeping for a heartbeat.")
            time.sleep(self.mSettings.get('heartbeat', 'period'))

    def insertRecvRequest(self, aMessageName, aCritthash, aMessage, aSoftTimeout=3, aHardTimeout=5):
        assert aCritthash not in self.mRecvReq[aMessageName], "Not handled yet. Duplicated critthash."
        self.mLogger.debug("Insert(ing) the recv request: [%s][%s]." % (aMessageName, aCritthash))
        self.mRecvReq[aMessageName][aCritthash] = aMessage

    def deleteRecvRequest(self, aMessageName, aCritthash):
        if aCritthash in self.mRecvReq[aMessageName]:
            self.mLogger.debug("Delete(ing) the recv request: [%s][%s]." % (aMessageName, aCritthash))
            del self.mRecvReq[aMessageName][aCritthash]

    def insertSentRequest(self, aMessageName, aCritthash, aEnvelope, aSoftTimeout=3, aHardTimeout=5):
        assert aCritthash not in self.mSentReq[aMessageName], "Not handled yet. Duplicated critthash."
        self.mLogger.debug("Insert(ing) the sent request: [%s][%s]." % (aMessageName, aCritthash))
        self.mSentReq[aMessageName][aCritthash] = {
            'envelope':    aEnvelope,
            'softTimeout': aSoftTimeout,
            'hardTimeout': aHardTimeout
        }
        self.mLogger.debug("Sending the %s message." % aMessageName)
        self.mPostOffice.putOutgoingAnnouncement(aEnvelope)

    def deleteSentRequest(self, aMessageName, aCritthash):
        if aCritthash in self.mSentReq[aMessageName]:
            self.mLogger.debug("Delete(ing) the sent request: [%s][%s]." % (aMessageName, aCritthash))
            del self.mSentReq[aMessageName][aCritthash]

    def getKnownCritters(self):
        """Returns the dictionary of known critters.

        Returns:
            The copy of the dictionary of known critters.
        """
        return copy.deepcopy(self.mKnownCrittnicks)

    def getNumberOfKnownCritters(self):
        """Returns the number of known critters.

        Returns The number of known critters.

        """
        return len(self.mKnownCrittnicks)
