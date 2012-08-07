"""The graph rite."""

import time

import Rites.RiteCommon

from Rites.Graph.GraphMessageProcessor import GraphMessageProcessor
from Rites.Rite                        import Rite

class GraphRite(Rite):
    """The graph rite.

    Attributes:
        mCommandProcessor: The command processor of the rite
        mMessageProcessor: The message processor of the rite
        mGraphs:           The graphs that are handled (a list).
        mWorks:            The works that are handled (a dictionary).
        mWorkPredecessors: The work predecessors that are handled (a dictionary).
        mSessions:         Running graph sessions (threads).

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
                      Rites.RiteCommon.GRAPH,
                      GraphMessageProcessor)

        self.mGraphs           = []
        self.mWorks            = {}
        self.mWorkPredecessors = {}

        self.mSessions = {}

    def run(self):
        """Starts the main loop of the rite."""

        # Ask for the configuration of graphs and works.
        envelope = self.mPostOffice.encode(
            'LoadGraphAndWorkRequest',
            {'messageName': 'LoadGraphAndWorkRequest',
             'sender':      {'type': self.mCritterData.mType,
                             'nick': self.mCritterData.mNick}})
        self.mPostOffice.putOutgoingAnnouncement(envelope)

        while True:
            self.mLogger.debug("Sleeping for a heartbeat.")

            # TODO: Remove me. For debug purposes only.
            if 'GraphName1' in self.mSessions:
                self.mLogger.debug("The number of sessions GraphName1: %d" % len(self.mSessions['GraphName1']))
            if 'GraphName2' in self.mSessions:
                self.mLogger.debug("The number of sessions GraphName2: %d" % len(self.mSessions['GraphName2']))
            if 'GraphName3' in self.mSessions:
                self.mLogger.debug("The number of sessions GraphName3: %d" % len(self.mSessions['GraphName3']))
            if 'GraphName4' in self.mSessions:
                self.mLogger.debug("The number of sessions GraphName4: %d" % len(self.mSessions['GraphName4']))

            time.sleep(self.mSettings.get('heartbeat', 'period'))
