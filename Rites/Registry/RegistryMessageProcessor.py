import Rites.RiteCommon

from Rites.MessageProcessor          import MessageProcessor
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

        if command:
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.REGISTRY, command)
        else:
            self.mLogger.debug("Dropping unknown message: %s" % aMessage.messageName)
