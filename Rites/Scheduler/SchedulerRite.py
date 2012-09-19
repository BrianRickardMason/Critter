import time

import Rites.RiteCommon

from Critter.PostOffice.SubscriptionChannels   import SUBSCRIPTION_CHANNEL_ALL
from Rites.Rite                                import Rite
from Rites.Scheduler.SchedulerCommands         import SchedulerCommand_Auto_CheckSchedule
from Rites.Scheduler.SchedulerCommands         import SchedulerCommand_Auto_LoadGraphAndWork
from Rites.Scheduler.SchedulerMessageProcessor import SchedulerMessageProcessor

class SchedulerRite(Rite):
    def __init__(self, aCritter, aSettings, aPostOffice):
        Rite.__init__(self,
                      aCritter,
                      aSettings,
                      aPostOffice,
                      Rites.RiteCommon.SCHEDULER,
                      SchedulerMessageProcessor)

        # Set the initial state of the rite.
        self.mState = Rites.RiteCommon.STATE_STARTING

        # Set subscription channels.
        self.mPostOffice.addSubscriptionChannel(SUBSCRIPTION_CHANNEL_ALL)

        # The dictionary of sent requests.
        self.mSentReq = {}
        self.mSentReq['Command_ExecuteGraph_Req'    ] = {}
        self.mSentReq['Command_LoadGraphAndWork_Req'] = {}
        self.mSentReq['Command_LoadGraphDetails_Req'] = {}
        self.mSentReq['Command_LoadWorkDetails_Req' ] = {}

        # Dictionaries of graph data.
        self.mGraphs       = []
        self.mGraphDetails = {}

        # Dictionaries of work data.
        self.mWorks            = {}
        self.mWorkDetails      = {}
        self.mWorkPredecessors = {}

    def run(self):
        while True:
            # TODO: Check the messages that timed out.

            self.mLogger.debug("Loading the data.")
            command = SchedulerCommand_Auto_LoadGraphAndWork()
            self.mPostOffice.putCommand(Rites.RiteCommon.SCHEDULER, command)

            self.mLogger.debug("Checking the schedule.")
            command = SchedulerCommand_Auto_CheckSchedule()
            self.mPostOffice.putCommand(Rites.RiteCommon.SCHEDULER, command)

            self.mLogger.debug("Sleeping for a heartbeat.")
            time.sleep(self.mSettings.get('heartbeat', 'period'))

    def setState(self, aState):
        self.mState = aState
