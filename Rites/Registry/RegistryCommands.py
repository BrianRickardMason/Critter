"""Registry rite commands."""

import time

from Critter.CritterData import CritterData

class RegistryCommandCheckHeartbeats(object):
    """RegisterCritter command.

    Attributes:
        mName The name of the command.

    """

    # TODO: If "there is not any heartbeat" twice and a critter is running, obviously something fishy is going on.

    def __init__(self):
        """Initializes the command."""
        self.mName = "RegistryCommandCheckHeartbeats"

    def execute(self, aCommandProcessor):
        """Executes the command.

        Arguments:
            aCommandProcessor: The command processor to be visited.

        """
        # FIXME: Jealous class.
        maxDelta =   aCommandProcessor.mRite.mSettings.get('heartbeat', 'maxDelay') \
                   * aCommandProcessor.mRite.mSettings.get('heartbeat', 'period')

        # Check if other critters are alive.
        # TODO: Check values vs. itervalues.
        for critterData in aCommandProcessor.mRite.mKnownCritters.values():
            nick = critterData.mNick

            if not nick in aCommandProcessor.mRite.mKnownCrittersHeartbeats:
                aCommandProcessor.mLogger.debug("Critter: %s. There is not any heartbeat from this critter yet." % nick)
            else:
                # Calculate the delta between heartbeat's.
                heartbeatDelta = time.time() - aCommandProcessor.mRite.mKnownCrittersHeartbeats[nick]
                aCommandProcessor.mLogger.debug("Critter: %s. Heartbeat's delta is %f." % (nick, heartbeatDelta))

                if heartbeatDelta > maxDelta:
                    aCommandProcessor.mLogger.warn("Critter: %s. Suspicious behavior." % nick)
                    aCommandProcessor.mLogger.warn("Critter: %s. Removing." % nick)
                    command = RegistryCommandUnregisterCritter(critterData)
                    aCommandProcessor.put(command)
                else:
                    aCommandProcessor.mLogger.debug("Critter: %s. Alive and kicking." % nick)

class RegistryCommandPresentYourself(object):
    """PresentYourself command.

    Attributes:
        mName:    The name of the command.
        mMessage: The PresentYourselfRequest.

    """

    def __init__(self, aMessage):
        """Initializes the command.

        Arguments:
            aMessage: The PresentYourselfRequest.

        """
        self.mName    = "RegistryCommandPresentYourself"
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        """Executes the command.

        Arguments:
            aCommandProcessor: The command processor to be visited.

        """
        if self.mMessage.receiver.nick == aCommandProcessor.mRite.mCritterData.mNick:
            receiverCritterData = CritterData(self.mMessage.sender.type, self.mMessage.sender.nick)

            envelope = aCommandProcessor.mRite.mPostOffice.encode(
                'PresentYourselfResponse',
                {'sender':   aCommandProcessor.mRite.mCritterData,
                 'receiver': receiverCritterData})
            aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)
        else:
            aCommandProcessor.mLogger.debug("The message is not addressed to me.")

class RegistryCommandRegisterCritter(object):
    """RegisterCritter command.

    Attributes:
        mName:    The name of the command.
        mMessage: The PresentYourselfResponse.

    """

    def __init__(self, aMessage):
        """Initializes the command.

        Arguments:
            aMessage: The PresentYourselfResponse.

        """
        self.mName    = "RegistryCommandRegisterCritter"
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        """Executes the command.

        Arguments:
            aCommandProcessor: The command processor to be visited.

        """
        if self.mMessage.receiver.nick == aCommandProcessor.mRite.mCritterData.mNick:
            critterData = CritterData(self.mMessage.sender.type, self.mMessage.sender.nick)
            nick = critterData.mNick

            if not nick in aCommandProcessor.mRite.mKnownCritters:
                aCommandProcessor.mLogger.debug("Critter: %s. Is not known." % nick)
                aCommandProcessor.mLogger.debug("Critter: %s. Registering." % nick)
                aCommandProcessor.mRite.mKnownCritters[nick] = critterData
            else:
                aCommandProcessor.mLogger.warn("Critter: %s. Is known. Should not send PresentYourselfResponse again."
                                               % nick)
        else:
            aCommandProcessor.mLogger.debug("The message is not addressed to me.")

class RegistryCommandStoreHeartbeat(object):
    """RegisterCritter command.

    Attributes:
        mName    The name of the command.
        mMessage The HeartbeatAnnouncement message.

    """

    def __init__(self, aMessage):
        """Initializes the command.

        Arguments:
            aMessage The HeartbeatAnnouncement message

        """
        self.mName    = "RegistryCommandStoreHeartbeat"
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        """Executes the command.

        Arguments:
            aCommandProcessor The command processor to be visited.

        """
        nick = self.mMessage.sender.nick

        if not nick in aCommandProcessor.mRite.mKnownCritters:
            aCommandProcessor.mLogger.debug("Critter: %s. I don't know you yet." % nick)

            unknownCritterData = CritterData(self.mMessage.sender.type, self.mMessage.sender.nick)

            envelope = aCommandProcessor.mRite.mPostOffice.encode(
                'PresentYourselfRequest',
                {'sender':   aCommandProcessor.mRite.mCritterData,
                 'receiver': unknownCritterData})
            aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)
        else:
            aCommandProcessor.mLogger.debug("Critter: %s. Storing the heartbeat's timestamp." % nick)
            aCommandProcessor.mRite.mKnownCrittersHeartbeats[nick] = self.mMessage.timestamp

class RegistryCommandUnregisterCritter(object):
    """UnregisterCritter command.

    Attributes:
        mName:        The name of the command.
        mCritterData: The critter's data.

    """

    def __init__(self, aCritterData):
        """Initializes the command.

        Arguments:
            aCritterData The critter's data

        """
        self.mName        = "RegistryCommandUnregisterCritter"
        self.mCritterData = aCritterData

    def execute(self, aCommandProcessor):
        """Executes the command.

        Arguments:
            aCommandProcessor: The command processor to be visited.

        """
        aCommandProcessor.mLogger.debug("Critter: %s. Unregistering." % self.mCritterData.mNick)
        # TODO: Verify how del behaves.
        nick = self.mCritterData.mNick

        # TODO: Check whether this check is needed at all!
        if nick in aCommandProcessor.mRite.mKnownCritters:
            del aCommandProcessor.mRite.mKnownCritters[nick]
        else:
            aCommandProcessor.mLogger.warn("Unknown nick in the table of known critters.")

        if nick in aCommandProcessor.mRite.mKnownCrittersHeartbeats:
            del aCommandProcessor.mRite.mKnownCrittersHeartbeats[nick]
        else:
            aCommandProcessor.mLogger.warn("Unknown nick in the table of known critters' heartbeats.")
