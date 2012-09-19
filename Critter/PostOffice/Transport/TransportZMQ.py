import zmq

from Transport import Transport
from Transport import TransportError

class TransportZMQ(Transport):
    def __init__(self, aAddressPublisher, aAddressSubscriber):
        # TODO: Add error handling.
        self.mCtx = zmq.Context()

        self.mSocketPublisher = self.mCtx.socket(zmq.PUB)
        self.mSocketPublisher.setsockopt(zmq.LINGER, 0)   # Discard unsent messages on close.
        self.mSocketPublisher.connect(aAddressPublisher)

        self.mSocketSubscriber = self.mCtx.socket(zmq.SUB)
        self.mSocketSubscriber.connect(aAddressSubscriber)
        self.mSocketSubscriber.setsockopt(zmq.SUBSCRIBE, '')

    def sendMessage(self, aSubscriptionChannel, aMessage):
        try:
            self.mSocketPublisher.send_multipart([aSubscriptionChannel, aMessage])
        except zmq.ZMQError:
            raise TransportError

    def recvMessage(self):
        return self.mSocketSubscriber.recv_multipart()
