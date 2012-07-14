"""The interface of transport."""

class TransportError(Exception):
    """The exception class for transport layer."""
    pass

class Transport(object):
    """The transport layer."""

    def sendAnnouncement(self, aMessage):
        """Sends an announcement that should reach all members of CrittWork.

        Arguments:
            aMessage: The message.

        Raises:
            TransportError: if something went wrong while sending.

        """
        raise NotImplementedError

    def recvAnnouncement(self):
        """Receives an announcement that was broadcasted.

        Returns:
            The bytes read.

        """
        raise NotImplementedError
