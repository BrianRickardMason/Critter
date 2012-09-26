import logging
import threading

from MessageDecoder import MessageDecoder

class AnnouncementSubscriber(threading.Thread):
    def __init__(self, aPostOffice):
        # Configuring the logger.
        self.mLogger = logging.getLogger(self.__class__.__name__)
        self.mLogger.propagate = False
        handler = logging.FileHandler('/tmp/' + aPostOffice.mCritter.mCrittnick + '.log')
        formatter = logging.Formatter('[%(asctime)s][%(threadName)28s][%(levelname)8s] - %(message)s')
        handler.setFormatter(formatter)
        self.mLogger.addHandler(handler)
        self.mLogger.setLevel(aPostOffice.mCritter.mSettings.get('logging', 'level'))

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
