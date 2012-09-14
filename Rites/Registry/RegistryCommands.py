import os
import time

import Rites.RiteCommon

from Critter.PostOffice.Priorities import PRIORITY_FAULT
from Critter.PostOffice.Priorities import PRIORITY_RECOVERY

class RegistryCommand_Auto_CheckHeartbeats(object):
    # TODO: If "there is not any heartbeat" twice and a critter is running, obviously something fishy is going on.
    def execute(self, aCommandProcessor):
        # FIXME: Jealous class.
        maxDelta =   aCommandProcessor.mRite.mSettings.get('heartbeat', 'maxDelay') \
                   * aCommandProcessor.mRite.mSettings.get('heartbeat', 'period')

        # Check if other critters are alive.
        # TODO: Check values vs. itervalues.
        for crittnick in aCommandProcessor.mRite.mKnownCrittnicks.values():
            if not crittnick in aCommandProcessor.mRite.mKnownHeartbeats:
                aCommandProcessor.mLogger.debug("Critter: %s. There is not any heartbeat from this critter yet."
                                                % crittnick)
            else:
                # Calculate the delta between heartbeat's.
                heartbeatDelta = time.time() - aCommandProcessor.mRite.mKnownHeartbeats[crittnick]
                aCommandProcessor.mLogger.debug("Critter: %s. Heartbeat's delta is %f." % (crittnick, heartbeatDelta))

                if heartbeatDelta > maxDelta:
                    aCommandProcessor.mLogger.warn("Critter: %s. Suspicious behavior." % crittnick)
                    aCommandProcessor.mLogger.warn("Critter: %s. Removing." % crittnick)
                    command = RegistryCommand_Fault_DeadCritter(crittnick)
                    aCommandProcessor.mRite.mPostOffice.putCommand(Rites.RiteCommon.REGISTRY, command, PRIORITY_FAULT)
                else:
                    aCommandProcessor.mLogger.debug("Critter: %s. Alive and kicking." % crittnick)

class RegistryCommand_Fault_DeadCritter(object):
    def __init__(self, aCrittnick):
        self.mCrittnick = aCrittnick

    def execute(self, aCommandProcessor):
        command = RegistryCommand_Recovery_UnregisterCritter(self.mCrittnick)
        aCommandProcessor.mRite.mPostOffice.putCommand(Rites.RiteCommon.REGISTRY, command, PRIORITY_RECOVERY)

class RegistryCommand_Handle_Announcement_Heartbeat(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mCritter.mCrittnick == self.mMessage.crittnick:
            return

        crittnick = self.mMessage.crittnick

        if not crittnick in aCommandProcessor.mRite.mKnownCrittnicks:
            aCommandProcessor.mLogger.debug("Critter: %s. I don't know you yet." % crittnick)

            messageName = 'Command_PresentYourself_Req'
            softTimeout = 3 # [s].
            hardTimeout = 5 # [s].
            critthash = os.urandom(32).encode('hex')
            message = aCommandProcessor.mRite.mPostOffice.encode({
                'messageName': messageName,
                'softTimeout': softTimeout,
                'hardTimeout': hardTimeout,
                'critthash':   critthash,
                'crittnick':   self.mMessage.crittnick
            })
            aCommandProcessor.mRite.insertSentRequest(messageName, critthash, message, softTimeout, hardTimeout)
        else:
            aCommandProcessor.mLogger.debug("Critter: %s. Storing the heartbeat's timestamp." % crittnick)
            aCommandProcessor.mRite.mKnownHeartbeats[crittnick] = self.mMessage.timestamp

class RegistryCommand_Handle_Command_PresentYourself_Req(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        if aCommandProcessor.mRite.mCritter.mCrittnick == self.mMessage.crittnick:
            messageNameRecvReq = self.mMessage.messageName
            critthash = self.mMessage.critthash
            aCommandProcessor.mRite.insertRecvRequest(messageNameRecvReq, critthash, self.mMessage)

            rites = []
            for riteName in aCommandProcessor.mRite.mCritter.mRites.keys():
                rites.append({'riteName': riteName})

            messageNameRecvRes = 'Command_PresentYourself_Res'
            message = aCommandProcessor.mRite.mPostOffice.encode({
                'messageName': messageNameRecvRes,
                'critthash':   critthash,
                'crittnick':   self.mMessage.crittnick,
                'rites':       rites
            })
            aCommandProcessor.mLogger.debug("Sending the %s message." % messageNameRecvRes)
            aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(message)

            aCommandProcessor.mRite.deleteRecvRequest(messageNameRecvReq, critthash)

class RegistryCommand_Handle_Command_PresentYourself_Res(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        messageNameSentReq = 'Command_PresentYourself_Req'
        critthash = self.mMessage.critthash
        crittnick = self.mMessage.crittnick
        if critthash in aCommandProcessor.mRite.mSentReq[messageNameSentReq]:
            if not crittnick in aCommandProcessor.mRite.mKnownCrittnicks:
                aCommandProcessor.mLogger.debug("Critter: %s is not known." % crittnick)
                aCommandProcessor.mLogger.debug("Critter: %s. Registering." % crittnick)
                aCommandProcessor.mRite.mKnownCrittnicks[crittnick] = crittnick

                rites = []
                for rite in self.mMessage.rites:
                    rites.append(rite.riteName)
                aCommandProcessor.mRite.mKnownRites[crittnick] = rites
            else:
                aCommandProcessor.mLogger.warn("Critter: %s is known." % crittnick)

            aCommandProcessor.mRite.deleteSentRequest(messageNameSentReq, critthash)

class RegistryCommand_Recovery_UnregisterCritter(object):
    def __init__(self, aCrittnick):
        self.mCrittnick = aCrittnick

    def execute(self, aCommandProcessor):
        aCommandProcessor.mLogger.debug("Critter: %s. Unregistering." % self.mCrittnick)
        # TODO: Verify how del behaves.

        # TODO: Check whether this check is needed at all!
        if self.mCrittnick in aCommandProcessor.mRite.mKnownCrittnicks:
            del aCommandProcessor.mRite.mKnownCrittnicks[self.mCrittnick]
        else:
            aCommandProcessor.mLogger.warn("Unknown crittnick in the table of known critters.")

        if self.mCrittnick in aCommandProcessor.mRite.mKnownHeartbeats:
            del aCommandProcessor.mRite.mKnownHeartbeats[self.mCrittnick]
        else:
            aCommandProcessor.mLogger.warn("Unknown nick in the table of known critters' heartbeats.")
