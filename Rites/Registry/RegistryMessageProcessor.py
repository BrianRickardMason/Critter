"""The message processor of registry rite."""

import Rites.RiteCommon

from Rites.MessageProcessor          import MessageProcessor
from Rites.Registry.RegistryCommands import RegistryCommandPresentYourself
from Rites.Registry.RegistryCommands import RegistryCommandRegisterCritter
from Rites.Registry.RegistryCommands import RegistryCommandStoreHeartbeat

class RegistryMessageProcessor(MessageProcessor):
    """The message processor of the registry rite."""

    def __init__(self, aRite):
        """Initializes the message processor.

        Arguments:
            aRite: The rite.

        """
        MessageProcessor.__init__(self, aRite)

    def processMessage(self, aMessage):
        """Processes the message.

        Arguments:
            aMessage: The message.

        """
        if aMessage.messageName == 'HeartbeatAnnouncement':
            command = RegistryCommandStoreHeartbeat(aMessage)
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.REGISTRY, command)

        elif aMessage.messageName == 'PresentYourselfRequest':
            command = RegistryCommandPresentYourself(aMessage)
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.REGISTRY, command)

        elif aMessage.messageName == 'PresentYourselfResponse':
            command = RegistryCommandRegisterCritter(aMessage)
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.REGISTRY, command)

        else:
            self.mLogger.debug("Dropping unknown message: %s" % aMessage.messageName)
