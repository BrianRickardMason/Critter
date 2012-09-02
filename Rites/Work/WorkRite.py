import time

import Rites.RiteCommon

from Rites.Work.WorkMessageProcessor import WorkMessageProcessor
from Rites.Rite                      import Rite

class WorkRite(Rite):
    def __init__(self, aCritter, aCritterData, aSettings, aPostOffice):
        Rite.__init__(self,
                      aCritter,
                      aCritterData,
                      aSettings,
                      aPostOffice,
                      Rites.RiteCommon.BALANCE,
                      WorkMessageProcessor)

        # A dictionary of received requests.
        self.mRecvReq = {}
        self.mRecvReq['Command_ExecuteWork_Req'] = {}

        # A dictionary of sent requests.
        self.mSentReq = {}
        self.mSentReq['Command_DetermineWorkCycle_Req'] = {}

        self.mWorkDetails = {}

        self.mSessions    = {}

    def run(self):
        # Request the load of the work details.
        envelope = self.mPostOffice.encode(
            'LoadWorkDetailsRequest',
            {'messageName': 'LoadWorkDetailsRequest',
             'sender':      {'type': self.mCritterData.mType,
                             'nick': self.mCritterData.mNick}})
        self.mPostOffice.putOutgoingAnnouncement(envelope)

        while True:
            self.mLogger.debug("Sleeping for a heartbeat.")
            time.sleep(self.mSettings.get('heartbeat', 'period'))
