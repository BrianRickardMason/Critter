"""Work rite commands."""

class WorkCommandInitializeWorkExecution(object):
    """InitializeWorkExecution command.

    Attributes:
        mName:    The name of the command.
        mMessage: The ExecuteWorkAnnouncement.

    """

    def __init__(self, aMessage):
        """Initializes the command.

        Arguments:
            aMessage: The ExecuteWorkAnnouncement.

        """
        self.mName    = 'WorkCommandInitializeWorkExecution'
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        """Executes the command.

        Arguments:
            aCommandProcessor: The command processor to be visited.

        """
        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            'DetermineWorkCycleRequest',
            {'sender':    aCommandProcessor.mRite.mCritterData,
             'graphName': self.mMessage.graphName,
             'cycle':     self.mMessage.cycle,
             'workName':  self.mMessage.workName})
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)
