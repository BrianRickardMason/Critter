import Rites.RiteCommon

from Rites.Balance.BalanceCommands import BalanceCommand_Handle_Command_Election_Res
from Rites.Balance.BalanceCommands import BalanceCommand_Handle_Command_ExecuteWork_Res
from Rites.Balance.BalanceCommands import BalanceCommand_Handle_Command_OrderWorkExecution_Req
from Rites.MessageProcessor        import MessageProcessor

class BalanceMessageProcessor(MessageProcessor):
    def __init__(self, aRite):
        MessageProcessor.__init__(self, aRite)

    def processMessage(self, aMessage):
        command = None

        if False: pass
        elif aMessage.messageName == 'Command_Election_Res':           command = BalanceCommand_Handle_Command_Election_Res(aMessage)
        elif aMessage.messageName == 'Command_ExecuteWork_Res':        command = BalanceCommand_Handle_Command_ExecuteWork_Res(aMessage)
        elif aMessage.messageName == 'Command_OrderWorkExecution_Req': command = BalanceCommand_Handle_Command_OrderWorkExecution_Req(aMessage)

        if command:
            self.mRite.mPostOffice.putCommand(Rites.RiteCommon.BALANCE, command)
        else:
            self.mLogger.debug("Dropping unknown message: %s" % aMessage.messageName)
