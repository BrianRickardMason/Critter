"""The balance rite."""

import time

import Rites.RiteCommon

from Rites.Balance.BalanceMessageProcessor import BalanceMessageProcessor
from Rites.Rite                            import Rite

# TODO: A generic mechanism to store sent and received messages (the information about them)!

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

        # CommandWorkExecution volunteering.
        #
        # It has a structure as follows:
        # {'hash': CritterHash,
        #  'data': data}
        #
        # data:
        # {'graphName':  string,
        #  'graphCycle': integer,
        #  'workName':   string,
        #  'boss':       string,
        #  'worker':     string}
        #
        self.mCommandWorkExecutionVolunteering = {}

        # A dictionary of elections.
        self.mElections = {}

        # A dictionary of received requests.
        self.mRecvReq = {}
        self.mRecvReq['Command_Req_OrderWorkExecution'] = {}

        # A dictionary of sent requests.
        self.mSentReq = {}
        self.mSentReq['Command_Req_Election'] = {}

    def run(self):
        """Starts the main loop of the rite."""
        while True:
            self.mLogger.debug("Sleeping for a heartbeat.")
            time.sleep(self.mSettings.get('heartbeat', 'period'))
