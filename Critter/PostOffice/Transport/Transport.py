class TransportError(Exception):
    pass

class Transport(object):
    def sendMessage(self, aSubscriptionChannel, aMessage):
        raise NotImplementedError

    def recvMessage(self):
        raise NotImplementedError

    def addSubscriptionChannel(self, aSubscriptionChannel):
        raise NotImplementedError

    def removeSubscriptionChannel(self, aSubscriptionChannel):
        raise NotImplementedError
