"""The message processor of balance rite."""

import Rites.RiteCommon

from Rites.Balance.BalanceCommands import BalanceCommand_Handle_CommandWorkExecutionSeekVolunteers
from Rites.Balance.BalanceCommands import BalanceCommand_Handle_CommandWorkExecutionSelectVolunteer
from Rites.Balance.BalanceCommands import BalanceCommand_Handle_Command_Req_OrderWorkExecution
from Rites.Balance.BalanceCommands import BalanceCommand_Handle_Command_Res_Election
from Rites.MessageProcessor        import MessageProcessor

class BalanceMessageProcessor(MessageProcessor):
    """The message processor of the balance rite."""

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
        command = None

        if False: pass
        elif aMessage.messageName == 'CommandWorkExecutionSeekVolunteers':  command = BalanceCommand_Handle_CommandWorkExecutionSeekVolunteers(aMessage)
        elif aMessage.messageName == 'CommandWorkExecutionSelectVolunteer': command = BalanceCommand_Handle_CommandWorkExecutionSelectVolunteer(aMessage)
        elif aMessage.messageName == 'Command_Req_OrderWorkExecution':      command = BalanceCommand_Handle_Command_Req_OrderWorkExecution(aMessage)
        elif aMessage.messageName == 'Command_Res_Election':                command = BalanceCommand_Handle_Command_Res_Election(aMessage)

        if command:
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.BALANCE, command)
        else:
            self.mLogger.debug("Dropping unknown message: %s" % aMessage.messageName)
