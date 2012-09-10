"""The essential critter's data."""

class CritterData(object):
    """Holds the essential critter's data.

    Attributes:
        mType The type.

    """

    def __init__(self, aType, aNick):
        """Initializes the data.

        Arguments:
            aType The type of the critter.

        """
        self.mType = aType
