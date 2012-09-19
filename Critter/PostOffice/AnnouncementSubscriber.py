"""The announcement subscriber."""

import logging
import threading

from MessageDecoder import MessageDecoder

logging.basicConfig(format='[%(asctime)s][%(threadName)28s][%(levelname)8s] - %(message)s')

class AnnouncementSubscriber(threading.Thread):
    """The subscriber of announcements that reach all critters.

    Attributes:
        mLogger:         The logger.
        mMessageDecoder: The message decoder.
        mPostOffice:     The post office.

    """

    def __init__(self, aPostOffice):
        """Initializes the announcement subscriber.

        Arguments:
            aPostOffice: The post office.

        """
        self.mLogger = logging.getLogger('AnnouncementSubscriber')
        self.mLogger.setLevel(logging.DEBUG)

        self.mPostOffice = aPostOffice

        self.mMessageDecoder = MessageDecoder()

        threading.Thread.__init__(self, name='AnnouncementSubscriber')

    def run(self):
        """Starts the main loop of the listener.

        Receives a message and puts it into the queue of incoming announcements. Repeats forever.

        """
        while True:
            # FIXME: A jealous class.
            [subscriptionChannel, bytesRead] = self.mPostOffice.mTransport.recvMessage()

            message = self.mMessageDecoder.decode(bytesRead)

            if message:
                self.mPostOffice.putIncomingAnnouncement(message)
            else:
                self.mLogger.warn("Invalid message received.")
