"""The essential critter's data."""

class CritterData(object):
    """Holds the essential critter's data.

    Attributes:
        mType The type.
        mNick The nick.

    """

    def __init__(self, aType, aNick):
        """Initializes the data.

        Arguments:
            aType The type of the critter.
            aNick The nick of the critter.

        """
        self.mType = aType
        self.mNick = aNick
