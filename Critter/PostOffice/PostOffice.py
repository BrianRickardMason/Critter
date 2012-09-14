"""The PostOffice that handles all the communication."""

import logging

from Queue import Queue

from AnnouncementPublisher  import AnnouncementPublisher
from AnnouncementSubscriber import AnnouncementSubscriber
from MessageEncoder         import MessageEncoder
from MessageRouter          import MessageRouter
from Priorities             import PRIORITY_DEFAULT
from RiteConnector          import RiteConnector
from Transport.TransportZMQ import TransportZMQ

logging.basicConfig(format='[%(asctime)s][%(threadName)28s][%(levelname)8s] - %(message)s')

class PostOffice(object):
    """The PostOffice that handles all the communication.

    Attributes:
        mCritter:                    The critter.
        mIncomingAnnouncementsQueue: The queue of incoming announcements.
        mLogger:                     The logger.
        mMessageEncoder:             The message encoder.
        mOutgoingAnnouncementsQueue: The queue of outgoing announcements.
        mAnnouncementPublisher:      The announcement publisher.
        mAnnouncementSubscriber:     The announcement subscriber.
        mMessageRouter:              The message router.
        mRiteConnector:              The rite connector.
        mTransport:                  The transport.

    """

    def __init__(self, aCritter):
        """Initializes the post office.

        Arguments:
            aCritter: The critter.

        """
        self.mCritter = aCritter

        settings = self.mCritter.getSettings()

        self.mLogger = logging.getLogger('PostOffice')
        self.mLogger.setLevel(self.mCritter.mSettings.get('logging', 'level'))

        policy = settings.get('crittwork', 'policy')

        addressPublisher = addressSubscriber = ''

        # TODO: Now this is an ifology, it should be a real policy.
        if policy == 'multicast':
            addressPublisher = addressSubscriber = settings.get('crittwork', 'multicast')
        elif policy == 'broker':
            addressPublisher  = settings.get('crittwork', 'brokerPublisher')
            addressSubscriber = settings.get('crittwork', 'brokerSubscriber')
        else:
            assert False, "Invalid crittwork policy selected."

        # TODO: Get from the factory.
        self.mTransport = TransportZMQ(addressPublisher, addressSubscriber)

        self.mOutgoingAnnouncementsQueue = Queue()
        self.mIncomingAnnouncementsQueue = Queue()

        self.mRiteConnector = RiteConnector(aCritter.mRites)

        self.mMessageEncoder = MessageEncoder()

        # Spawning the announcement publisher.
        self.mLogger.debug("Spawning the announcement publisher.")
        self.mAnnouncementPublisher = AnnouncementPublisher(self)
        self.mAnnouncementPublisher.setDaemon(True)

        # Spawning the announcement subscriber.
        self.mLogger.debug("Spawning the announcement subscriber.")
        self.mAnnouncementSubscriber = AnnouncementSubscriber(self)
        self.mAnnouncementSubscriber.setDaemon(True)

        # Spawning the message router.
        # FIXME: Jealous class.
        self.mLogger.debug("Spawning the message router.")
        self.mMessageRouter = MessageRouter(self)
        self.mMessageRouter.setDaemon(True)

    def start(self):
        """Starts the post office by starting its threads."""
        self.mAnnouncementPublisher.start()
        self.mAnnouncementSubscriber.start()
        self.mMessageRouter.start()

    def encode(self, aData):
        """A facade method to hide message encoder from clients.

        Arguments:
            aData: The dictionary of parameters.

        Returns:
            A message.

        """
        return self.mMessageEncoder.encode(aData)

    def putIntoAnEnvelope(self, aMessage):
        return self.mMessageEncoder.putIntoAnEnvelope(aMessage)

    def putIncomingAnnouncement(self, aMessage):
        """Puts an incoming announcement (in the form of a message class) into the queue.

        Arguments:
            aMessage The message to be processed.

        """
        self.mIncomingAnnouncementsQueue.put(aMessage)

    def putOutgoingAnnouncement(self, aMessage):
        """Puts an outgoing announcement (in the form of a message class) into the queue.

        Arguments:
            aMessage The message to be sent.

        """
        self.mOutgoingAnnouncementsQueue.put(aMessage)

    def getIncomingAnnouncement(self):
        """Gets an incoming announcement (in the form of a message class) from the queue.

        Returns The message to be processed.

        """
        return self.mIncomingAnnouncementsQueue.get()

    def getOutgoingAnnouncement(self):
        """Gets an outgoing announcement (in the form of a message class) from the queue.

        Returns The message to be sent.

        """
        return self.mOutgoingAnnouncementsQueue.get()

    def putCommand(self, aRite, aCommand, aPriority=PRIORITY_DEFAULT):
        self.mRiteConnector.putCommand(aRite, aCommand, aPriority)

    def putMessage(self, aRite, aMessage, aPriority=PRIORITY_DEFAULT):
        self.mRiteConnector.putMessage(aRite, aMessage, aPriority)
