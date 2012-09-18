"""The broadcast daemon."""

# TODO: Should abstract from the transport as well.

import logging
import threading
# TODO: Import of time should not be needed.
import time
import zmq

from Critter.PostOffice import MessageDecoder
from Queue              import Queue

logging.basicConfig(format='[%(asctime)s][%(threadName)15s][%(levelname)8s] - %(message)s')

class Publisher(threading.Thread):
    """The publisher of broadcast daemon.

    Attributes:
        mLogger:          The logger.
        mSocket:          The socket to subscribe.
        mBroadcastDaemon: The broadcast daemon.

    """

    def __init__(self, aBroadcastDaemon):
        """Initializes the publisher.

        Arguments:
            aBroadcastDaemon: The broadcast daemon.

        """
        self.mLogger = logging.getLogger('Publisher')
        self.mLogger.setLevel(logging.DEBUG)

        self.mBroadcastDaemon = aBroadcastDaemon

        self.mSocket = aBroadcastDaemon.mCtx.socket(zmq.PUB)
        # FIXME: Remove the hardcoded value.
        self.mSocket.bind('tcp://*:4444')

        threading.Thread.__init__(self, name='Publisher')

    def run(self):
        """Starts the main loop of the publisher.

        Gets bytes from the queue sends it. Repeats forever.

        """
        #
        # A simple performance test on i7 4.2 GHz has shown that if each message were decoded 1000 times,
        # then it would be too much for Crittwork of 5 elements and there would be delays. However, for now we will
        # apply ostrich algorithm and the logic that stands behind message routing will be fully located in
        # the BroadcastDaemon. This way the architecture of Crittwork stays untouched.
        #
        messageDecoder = MessageDecoder.MessageDecoder()

        while True:
            bytesRead = self.mBroadcastDaemon.mQueue.get()
            self.mSocket.send(bytesRead)

            message = messageDecoder.decode(bytesRead)
            # TODO: Implement me in a more beautiful way.
            if message.messageName == 'Command_DescribeCrittwork_Res':
                self.mBroadcastDaemon.mResponder.respond(bytesRead)

class Subscriber(threading.Thread):
    """The subscriber of broadcast daemon.

    Attributes:
        mLogger:          The logger.
        mSocket:          The socket to subscribe.
        mBroadcastDaemon: The broadcast daemon.

    """

    def __init__(self, aBroadcastDaemon):
        """Initializes the subscriber.

        Arguments:
            aBroadcastDaemon: The broadcast daemon.

        """
        self.mLogger = logging.getLogger('Subscriber')
        self.mLogger.setLevel(logging.DEBUG)

        self.mBroadcastDaemon = aBroadcastDaemon

        self.mSocket = aBroadcastDaemon.mCtx.socket(zmq.SUB)
        # FIXME: Remove the hardcoded value.
        self.mSocket.bind('tcp://127.0.0.1:2222')
        self.mSocket.setsockopt(zmq.SUBSCRIBE, '')

        threading.Thread.__init__(self, name='Subscriber')

    def run(self):
        """Starts the main loop of the subscriber.

        Receives bytes from the socket and puts them it into the queue. Repeats forever.

        """
        while True:
            bytesRead = self.mSocket.recv()
            self.mBroadcastDaemon.mQueue.put(bytesRead)

class Responder(threading.Thread):
    def __init__(self, aBroadcastDaemon):
        self.mLogger = logging.getLogger('Responder')
        self.mLogger.setLevel(logging.DEBUG)

        self.mBroadcastDaemon = aBroadcastDaemon

        self.mSocket = aBroadcastDaemon.mCtx.socket(zmq.PAIR)
        # FIXME: Remove the hardcoded value.
        self.mSocket.bind('tcp://127.0.0.1:5555')

        threading.Thread.__init__(self, name='Responder')

    def run(self):
        while True:
            # TODO: Add registration of requests (so that you'd know whom to answer).
            # TODO: Discuss the sequence of messages.
            bytesRead = self.mSocket.recv()
            self.mBroadcastDaemon.mQueue.put(bytesRead)

    def respond(self, aBytes):
        self.mSocket.send(aBytes)

class BroadcastDaemon(object):
    """The broadcast daemon.

    Attributes:
        mCtx:        The 0MQ context.
        mQueue:      The queue of read bytes.
        mSubscriber: The subscriber.
        mPublisher:  The publisher.

    """

    def __init__(self):
        """Initializes the post office.

        Arguments:
            aCritter: The critter.

        """
        self.mLogger = logging.getLogger('BroadcastDaemon')
        self.mLogger.setLevel(logging.DEBUG)

        self.mCtx = zmq.Context()

        self.mQueue = Queue()

        # Spawning the publisher.
        self.mLogger.debug("Spawning the publisher.")
        self.mPublisher = Publisher(self)
        self.mPublisher.setDaemon(True)
        self.mPublisher.start()

        # Spawning the subscriber.
        self.mLogger.debug("Spawning the subscriber.")
        self.mSubscriber = Subscriber(self)
        self.mSubscriber.setDaemon(True)
        self.mSubscriber.start()

        # Spawning the responder.
        self.mLogger.debug("Spawning the responder.")
        self.mResponder = Responder(self)
        self.mResponder.setDaemon(True)
        self.mResponder.start()

    def run(self):
        while True:
            # FIXME: Do it somehow different.
            time.sleep(1)

if __name__ == "__main__":
    broadcastDaemon = BroadcastDaemon()
    broadcastDaemon.run()
