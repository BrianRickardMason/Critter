"""The announcement publisher."""

import logging
import threading

from Transport.Transport import TransportError

logging.basicConfig(format='[%(asctime)s][%(threadName)28s][%(levelname)8s] - %(message)s')

class AnnouncementPublisher(threading.Thread):
    """The publisher of announcements that reach all critters.

    Attributes:
        mLogger:     The logger.
        mPostOffice: The post office.

    """

    def __init__(self, aPostOffice):
        """Initializes the announcement publisher.

        Arguments:
            aPostOffice: The post office.

        """
        self.mLogger = logging.getLogger('AnnouncementPublisher')
        self.mLogger.setLevel(logging.DEBUG)

        self.mPostOffice = aPostOffice

        threading.Thread.__init__(self, name='AnnouncementPublisher')

    def run(self):
        """Starts the main loop of the announcement publisher.

        Gets a message from the queue of outgoing announcements and sends it. Repeats forever.

        """
        while True:
            envelope = self.mPostOffice.getOutgoingAnnouncement()

            message = envelope.SerializeToString()

            try:
                # FIXME: A jealous class.
                self.mPostOffice.mTransport.sendAnnouncement(message)
            except TransportError, e:
                self.mLogger.warn("An error occurred while sending the message: %s." % e)
