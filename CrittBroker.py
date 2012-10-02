import logging
import sys
import threading
import zmq

from Queue    import Queue
from optparse import OptionParser

from Critter.PostOffice.SubscriptionChannels import SUBSCRIPTION_CHANNEL_ALL
from Critter.PostOffice                      import MessageDecoder

# FIXME: Different convention changed (to 28). Needed to propagate.
logging.basicConfig(format='[%(asctime)s][%(threadName)28s][%(levelname)8s] - %(message)s')

# TODO: Should abstract from the transport as well.

class Publisher(threading.Thread):
    def __init__(self, aCrittBroker, aAddress):
        self.mCrittBroker = aCrittBroker

        self.mSocket = aCrittBroker.mCtx.socket(zmq.PUB)
        self.mSocket.bind(aAddress)

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
    def __init__(self, aCrittBroker, aAddress):
        self.mCrittBroker = aCrittBroker

        self.mSocket = aCrittBroker.mCtx.socket(zmq.SUB)
        self.mSocket.bind(aAddress)
        self.mSocket.setsockopt(zmq.SUBSCRIBE, '')

        threading.Thread.__init__(self, name='Subscriber')

    def run(self):
        while True:
            [subscriptionChannel, bytesRead] = self.mSocket.recv_multipart()
            self.mCrittBroker.mQueue.put([subscriptionChannel, bytesRead])
            self.mCrittBroker.mCrittBrokerTubePubQueue.put([subscriptionChannel, bytesRead])

class Responder(threading.Thread):
    def __init__(self, aCrittBroker, aAddress):
        self.mCrittBroker = aCrittBroker

        # TODO: Pair is not recommended. Change it.
        self.mSocket = aCrittBroker.mCtx.socket(zmq.PAIR)
        self.mSocket.bind(aAddress)

        threading.Thread.__init__(self, name='Responder')

    def run(self):
        while True:
            # TODO: Responder won't work correctly yet (it needs to be specified via parameters).
            # TODO: Add registration of requests (so that you'd know whom to answer).
            # TODO: Discuss the sequence of messages.
            bytesRead = self.mSocket.recv()
            # FIXME: Remove the hardcoded value of the subscription channel.
            self.mCrittBroker.mQueue.put([SUBSCRIPTION_CHANNEL_ALL, bytesRead])

    def respond(self, aBytes):
        self.mSocket.send(aBytes)

class CrittBrokerTubePub(threading.Thread):
    def __init__(self, aCrittBroker, aAddress):
        self.mCrittBroker = aCrittBroker

        self.mSocket = self.mCrittBroker.mCtx.socket(zmq.PUB)
        self.mSocket.bind(aAddress)

        threading.Thread.__init__(self, name='CrittBrokerTubePub')

    def run(self):
        while True:
            self.mCrittBroker.mLogger.info("Publishing %s" % self.mCrittBroker.mName)
            [subscriptionChannel, bytesRead] = self.mCrittBroker.mCrittBrokerTubePubQueue.get()
            self.mSocket.send_multipart([subscriptionChannel, bytesRead])

class CrittBrokerTubeSub(threading.Thread):
    def __init__(self, aCrittBroker, aAddress):
        self.mCrittBroker = aCrittBroker

        self.mSocket = self.mCrittBroker.mCtx.socket(zmq.SUB)
        self.mSocket.connect(aAddress)
        self.mSocket.setsockopt(zmq.SUBSCRIBE, '')

        threading.Thread.__init__(self, name='CrittBrokerTubeSub')

    def run(self):
        while True:
            [subscriptionChannel, bytesRead] = self.mSocket.recv_multipart()
            self.mCrittBroker.mQueue.put([subscriptionChannel, bytesRead])

class CrittBroker(object):
    def __init__(self, aArgv):
        # Parse the options.
        usage = "Usage: %prog [options]"
        parser = OptionParser(usage)
        parser.add_option("--name",          dest="name",          help="the name of the broker")
        parser.add_option("--host",          dest="host",          help="the name of the host")
        parser.add_option("--publish",       dest="publish",       help="the CrittWork address of the publisher")
        parser.add_option("--subscribe",     dest="subscribe",     help="the CrittWork address of the subscriber")
        parser.add_option("--ui",            dest="ui",            help="the CrittWork address of the ui interface")
        parser.add_option("--brokerPublish", dest="brokerPublish", help="the CrittWork address of the CrittBrokerTubePub interface")
        parser.add_option("--broker",        action="append",
                                             dest="broker",        help="the CrittWork address of another broker that the broker should listen to")
        # TODO: Make it more safe, remark mandatory parameters, etc.
        (options, args) = parser.parse_args()
        if len(args) != 0:
            parser.error("incorrect number of arguments")

        self.mName = options.name
        self.mHost = options.host

        self.mLogger = logging.getLogger(self.__class__.__name__)
        self.mLogger.propagate = False
        handler = logging.FileHandler('/tmp/' + self.mName + '.log')
        formatter = logging.Formatter('[%(asctime)s][%(threadName)28s][%(levelname)8s] - %(message)s')
        handler.setFormatter(formatter)
        self.mLogger.addHandler(handler)
        self.mLogger.setLevel(logging.DEBUG)

        self.mCtx = zmq.Context()

        self.mQueue = Queue()
        self.mCrittBrokerTubePubQueue = Queue()

        self.mCrittBrokerTubesSub = {}

        self.mLogger.debug("Spawning the publisher.")
        self.mPublisher = Publisher(self, options.publish)
        self.mPublisher.setDaemon(True)
        self.mPublisher.start()

        self.mLogger.debug("Spawning the subscriber.")
        self.mSubscriber = Subscriber(self, options.subscribe)
        self.mSubscriber.setDaemon(True)
        self.mSubscriber.start()

        # TODO: Common naming convention.
        self.mLogger.debug("Spawning the responder.")
        self.mResponder = Responder(self, options.ui)
        self.mResponder.setDaemon(True)
        self.mResponder.start()

        self.mLogger.debug("Spawning the CrittBrokerTubePub.")
        self.mCrittBrokerTubePub = CrittBrokerTubePub(self, options.brokerPublish)
        self.mCrittBrokerTubePub.setDaemon(True)
        self.mCrittBrokerTubePub.start()

        if options.broker:
            for brokerOption in options.broker:
                brokerOptions = brokerOption.split(',')
                self.mLogger.info("Spawning the CrittBrokerTubeSub to CrittBroker %s." % brokerOptions[0])
                self.mCrittBrokerTubesSub[brokerOptions[0]] = CrittBrokerTubeSub(self, brokerOptions[1])
                self.mCrittBrokerTubesSub[brokerOptions[0]].setDaemon(True)
                self.mCrittBrokerTubesSub[brokerOptions[0]].start()

    def run(self):
        self.mPublisher.join()
        self.mSubscriber.join()
        self.mResponder.join()

if __name__ == "__main__":
    crittBroker = CrittBroker(sys.argv)
    crittBroker.run()
