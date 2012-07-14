"""The 0MQ based transport."""

import zmq

from Transport import Transport
from Transport import TransportError

class TransportZMQ(Transport):
    """The 0MQ based transport layer.

    Attributes:
        mCtx:                          The ZMQ context.
        mSocketAnnouncementSubscriber: The socket of announcement subscriber.
        mSocketAnnouncementPublisher:  The socket of announcement publisher.

    """

    def __init__(self, aAddressPublisher, aAddressSubscriber):
        """Initializes the 0MQ transport layer.

        Arguments:
            aAddressPublisher:  The address that announcements are sent to (in a form of string).
            aAddressSubscriber: The address that announcements come from (in a form of string).

        """
        # TODO: Add error handling.
        self.mCtx = zmq.Context()

        self.mSocketAnnouncementPublisher = self.mCtx.socket(zmq.PUB)
        self.mSocketAnnouncementPublisher.setsockopt(zmq.LINGER, 0)   # Discard unsent messages on close.
        self.mSocketAnnouncementPublisher.connect(aAddressPublisher)

        self.mSocketAnnouncementSubscriber = self.mCtx.socket(zmq.SUB)
        self.mSocketAnnouncementSubscriber.connect(aAddressSubscriber)
        self.mSocketAnnouncementSubscriber.setsockopt(zmq.SUBSCRIBE, '')

    def sendAnnouncement(self, aMessage):
        """Sends an announcement that should reach all members of CrittWork.

        Arguments:
            aMessage: The message.

        Raises:
            TransportError: if something went wrong while sending.

        """
        try:
            self.mSocketAnnouncementPublisher.send(aMessage)
        except zmq.ZMQError:
            raise TransportError

    def recvAnnouncement(self):
        """Receives an announcement that was broadcasted.

        Returns:
            The bytes read.

        """
        return self.mSocketAnnouncementSubscriber.recv()
