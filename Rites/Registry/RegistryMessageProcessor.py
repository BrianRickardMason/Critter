import Rites.RiteCommon

from Rites.MessageProcessor          import MessageProcessor
from Rites.Registry.RegistryCommands import RegistryCommandPresentYourself
from Rites.Registry.RegistryCommands import RegistryCommandRegisterCritter
from Rites.Registry.RegistryCommands import RegistryCommandStoreHeartbeat
from Rites.Registry.RegistryCommands import RegistryCommand_Handle_Announcement_Heartbeat
from Rites.Registry.RegistryCommands import RegistryCommand_Handle_Command_PresentYourself_Req
from Rites.Registry.RegistryCommands import RegistryCommand_Handle_Command_PresentYourself_Res

class RegistryMessageProcessor(MessageProcessor):
    def __init__(self, aRite):
        MessageProcessor.__init__(self, aRite)

    def processMessage(self, aMessage):
        command = None

        if aMessage.messageName == 'Announcement_Heartbeat':
            command = RegistryCommand_Handle_Announcement_Heartbeat(aMessage)
        elif aMessage.messageName == 'Command_PresentYourself_Req':
            command = RegistryCommand_Handle_Command_PresentYourself_Req(aMessage)
        elif aMessage.messageName == 'Command_PresentYourself_Res':
            command = RegistryCommand_Handle_Command_PresentYourself_Res(aMessage)
        elif aMessage.messageName == 'HeartbeatAnnouncement':
            command = RegistryCommandStoreHeartbeat(aMessage)
        elif aMessage.messageName == 'PresentYourselfRequest':
            command = RegistryCommandPresentYourself(aMessage)
        elif aMessage.messageName == 'PresentYourselfResponse':
            command = RegistryCommandRegisterCritter(aMessage)

        if command:
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.REGISTRY, command)
        else:
            self.mLogger.debug("Dropping unknown message: %s" % aMessage.messageName)
