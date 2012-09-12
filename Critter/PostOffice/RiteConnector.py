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

    def putCommand(self, aRite, aCommand, aPriority):
        # TODO: Make sure the exceptions are handled!
        if aRite in self.mRites:
            self.mRites[aRite].putCommand(aCommand, aPriority)
        else:
            raise ValueError("There is not such a rite.")

    def putMessage(self, aRite, aMessage, aPriority):
        # TODO: Make sure the exceptions are handled!
        if aRite in self.mRites:
            self.mRites[aRite].putMessage(aMessage, aPriority)
        else:
            raise ValueError("There is not such a rite.")
