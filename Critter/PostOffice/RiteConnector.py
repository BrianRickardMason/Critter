"""The RiteConnector that is responsible for all communication between rites.

Both types: messages and commands are routed here.

"""

class RiteConnector(object):
    """The RiteConnector.

    Attributes:
        mRites: The dictionary of rites.

    """

    def __init__(self, aRites):
        """Initializes the command office.

        Arguments:
            aRites: The dictionary of rites.

        """
        self.mRites = aRites

    def putCommand(self, aRite, aCommand):
        """Puts a command to be processed by a rite.

        Arguments:
            aRite: The name of the rite.
            aCommand: The command to be processed by the rite.

        Raises:
            ValueError: if there is no rite of such a name.

        """
        # TODO: Make sure the exceptions are handled!
        if aRite in self.mRites:
            self.mRites[aRite].putCommand(aCommand)
        else:
            raise ValueError("There is not such a rite.")

    def putMessage(self, aRite, aMessage):
        """Puts a message to be processed by a rite.

        Arguments:
            aRite: The name of the rite.
            aMessage: The message to be processed by the rite.

        Raises:
            ValueError: if there is no rite of such a name.

        """
        # TODO: Make sure the exceptions are handled!
        if aRite in self.mRites:
            self.mRites[aRite].putMessage(aMessage)
        else:
            raise ValueError("There is not such a rite.")
