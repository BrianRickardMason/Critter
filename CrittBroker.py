import logging
import sys
import threading
import zmq

from Critter.PostOffice.SubscriptionChannels import SUBSCRIPTION_CHANNEL_ALL
from Critter.PostOffice                      import MessageDecoder
from Queue                                   import Queue

logging.basicConfig(format='[%(asctime)s][%(threadName)15s][%(levelname)8s] - %(message)s')

# TODO: Should abstract from the transport as well.

class Publisher(threading.Thread):
    def __init__(self, aCrittBroker, aProtocol, aPort):
        self.mCrittBroker = aCrittBroker

        self.mSocket = aCrittBroker.mCtx.socket(zmq.PUB)
        self.mSocket.bind(aProtocol + '*:' + aPort)

        threading.Thread.__init__(self, name='Publisher')

    def run(self):
        #
        # A simple performance test on i7 4.2 GHz has shown that if each message were decoded 1000 times,
        # then it would be too much for Crittwork of 5 elements and there would be delays. However, for now we will
        # apply ostrich algorithm and the logic that stands behind message routing will be fully located in
        # the CrittBroker. This way the architecture of Crittwork stays untouched.
        #
        messageDecoder = MessageDecoder.MessageDecoder()

        while True:
            [subscriptionChannel, bytesRead] = self.mCrittBroker.mQueue.get()
            self.mSocket.send_multipart([subscriptionChannel, bytesRead])

            message = messageDecoder.decode(bytesRead)
            # TODO: Implement me in a more beautiful way.
            if message.messageName == 'Command_DescribeCrittwork_Res':
                self.mCrittBroker.mResponder.respond(bytesRead)

class Subscriber(threading.Thread):
    def __init__(self, aCrittBroker, aProtocol, aPort):
        self.mCrittBroker = aCrittBroker

        self.mSocket = aCrittBroker.mCtx.socket(zmq.SUB)
        self.mSocket.bind(aProtocol + aCrittBroker.mHost + ':' + aPort)
        self.mSocket.setsockopt(zmq.SUBSCRIBE, '')

        threading.Thread.__init__(self, name='Subscriber')

    def run(self):
        while True:
            [subscriptionChannel, bytesRead] = self.mSocket.recv_multipart()
            self.mCrittBroker.mQueue.put([subscriptionChannel, bytesRead])

class Responder(threading.Thread):
    def __init__(self, aCrittBroker, aProtocol, aPort):
        self.mCrittBroker = aCrittBroker

        self.mSocket = aCrittBroker.mCtx.socket(zmq.PAIR)
        self.mSocket.bind(aProtocol + aCrittBroker.mHost + ':' + aPort)

        threading.Thread.__init__(self, name='Responder')

    def run(self):
        while True:
            # TODO: Add registration of requests (so that you'd know whom to answer).
            # TODO: Discuss the sequence of messages.
            bytesRead = self.mSocket.recv()
            # FIXME: Remove the hardcoded value of the subscription channel.
            self.mCrittBroker.mQueue.put([SUBSCRIPTION_CHANNEL_ALL, bytesRead])

    def respond(self, aBytes):
        self.mSocket.send(aBytes)

class CrittBroker(object):
    def __init__(self, aArgv):
        # TODO: Further analysis of parameters.
        if len(aArgv) != 9:
            # TODO: Make meaningful.
            raise Exception

        self.mName = aArgv[1]
        self.mHost = aArgv[2]

        self.mLogger = logging.getLogger(self.__class__.__name__)
        self.mLogger.propagate = False
        handler = logging.FileHandler('/tmp/' + aArgv[1] + '.log')
        formatter = logging.Formatter('[%(asctime)s][%(threadName)28s][%(levelname)8s] - %(message)s')
        handler.setFormatter(formatter)
        self.mLogger.addHandler(handler)
        self.mLogger.setLevel(logging.DEBUG)

        self.mCtx = zmq.Context()

        self.mQueue = Queue()

        self.mLogger.debug("Spawning the publisher.")
        self.mPublisher = Publisher(self, aArgv[3], aArgv[4])
        self.mPublisher.setDaemon(True)
        self.mPublisher.start()

        self.mLogger.debug("Spawning the subscriber.")
        self.mSubscriber = Subscriber(self, aArgv[5], aArgv[6])
        self.mSubscriber.setDaemon(True)
        self.mSubscriber.start()

        # TODO: Common naming convention.
        self.mLogger.debug("Spawning the responder.")
        self.mResponder = Responder(self, aArgv[7], aArgv[8])
        self.mResponder.setDaemon(True)
        self.mResponder.start()

    def run(self):
        self.mPublisher.join()
        self.mSubscriber.join()
        self.mResponder.join()

if __name__ == "__main__":
    crittBroker = CrittBroker(sys.argv)
    crittBroker.run()
