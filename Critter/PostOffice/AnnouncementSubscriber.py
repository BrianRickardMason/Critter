import logging
import threading

from MessageDecoder import MessageDecoder

logging.basicConfig(format='[%(asctime)s][%(threadName)28s][%(levelname)8s] - %(message)s')

class AnnouncementSubscriber(threading.Thread):
    def __init__(self, aPostOffice):
        self.mLogger = logging.getLogger('AnnouncementSubscriber')
        self.mLogger.setLevel(logging.DEBUG)

        self.mPostOffice = aPostOffice

        self.mMessageDecoder = MessageDecoder()

        threading.Thread.__init__(self, name='AnnouncementSubscriber')

    def run(self):
        while True:
            # FIXME: A jealous class.
            [subscriptionChannel, serializedEnvelope] = self.mPostOffice.mTransport.recvMessage()

            message = self.mMessageDecoder.decode(serializedEnvelope)

            if message:
                self.mPostOffice.putIncomingAnnouncement(message)
            else:
                self.mLogger.warn("Invalid message received.")
