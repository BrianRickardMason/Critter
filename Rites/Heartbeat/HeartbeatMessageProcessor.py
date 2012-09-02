from Rites.MessageProcessor import MessageProcessor

class HeartbeatMessageProcessor(MessageProcessor):
    def __init__(self, aRite):
        MessageProcessor.__init__(self, aRite)

    def processMessage(self, aMessage):
        self.mLogger.debug("Dropping unknown message: %s" % aMessage.messageName)
