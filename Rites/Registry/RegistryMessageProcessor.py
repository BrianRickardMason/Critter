import Rites.RiteCommon

from Rites.MessageProcessor          import MessageProcessor
from Rites.Registry.RegistryCommands import RegistryCommandPresentYourself
from Rites.Registry.RegistryCommands import RegistryCommandRegisterCritter
from Rites.Registry.RegistryCommands import RegistryCommandStoreHeartbeat

class RegistryMessageProcessor(MessageProcessor):
    def __init__(self, aRite):
        MessageProcessor.__init__(self, aRite)

    def processMessage(self, aMessage):
        command = None

        if False: pass
        elif aMessage.messageName == 'HeartbeatAnnouncement':   command = RegistryCommandStoreHeartbeat(aMessage)
        elif aMessage.messageName == 'PresentYourselfRequest':  command = RegistryCommandPresentYourself(aMessage)
        elif aMessage.messageName == 'PresentYourselfResponse': command = RegistryCommandRegisterCritter(aMessage)

        if command:
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.REGISTRY, command)
        else:
            self.mLogger.debug("Dropping unknown message: %s" % aMessage.messageName)
