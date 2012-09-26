import logging
import threading

from Transport.Transport import TransportError

logging.basicConfig(format='[%(asctime)s][%(threadName)28s][%(levelname)8s] - %(message)s')

class AnnouncementPublisher(threading.Thread):
    def __init__(self, aPostOffice):
        self.mLogger = logging.getLogger('AnnouncementPublisher')
        self.mLogger.setLevel(logging.DEBUG)

        self.mPostOffice = aPostOffice

        threading.Thread.__init__(self, name='AnnouncementPublisher')

    def run(self):
        while True:
            # The message sending algorithm.
            # 1. Get a message.
            # 2. Put it into an envelope.
            # 3. Serialize the envelope.
            # 4. Find a corresponding subscription channel.
            # 5. Send the subscription channel / serialized envelope pair.

            # Step 1.
            message = self.mPostOffice.getOutgoingAnnouncement()

            # Step 2.
            envelope = self.mPostOffice.putIntoAnEnvelope(message)

            # Step 3.
            serializedEnvelope = envelope.SerializeToString()

            # Step 4.
            subscriptionChannel = self.mPostOffice.getCorrespondingSubscriptionChannel(message)

            try:
                # Step 5.
                # FIXME: A jealous class.
                self.mPostOffice.mTransport.sendMessage(subscriptionChannel, serializedEnvelope)
            except TransportError, e:
                self.mLogger.warn("An error occurred while sending the message: %s." % e)
