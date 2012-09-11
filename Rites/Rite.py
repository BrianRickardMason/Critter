import logging
import threading
import time

from Rites.CommandProcessor import CommandProcessor

logging.basicConfig(format='[%(asctime)s][%(threadName)28s][%(levelname)8s] - %(message)s')

class Rite(threading.Thread):
    def __init__(self, aCritter, aSettings, aPostOffice, aRiteName, aMessageProcessorType):
        self.mSettings = aSettings

        self.mLogger = logging.getLogger(aRiteName + 'Rite')
        self.mLogger.setLevel(self.mSettings.get('logging', 'level'))

        self.mCritter    = aCritter
        self.mPostOffice = aPostOffice
        self.mRiteName   = aRiteName

        self.mLogger.info("Spawning the command processor.")
        self.__mCommandProcessor = CommandProcessor(self)
        self.__mCommandProcessor.setDaemon(True)
        self.__mCommandProcessor.start()

        self.mLogger.info("Spawning the message processor.")
        self.__mMessageProcessor = aMessageProcessorType(self)
        self.__mMessageProcessor.setDaemon(True)
        self.__mMessageProcessor.start()

        threading.Thread.__init__(self, name=aRiteName + 'Rite')

    def run(self):
        raise NotImplementedError

    # FIXME: A magic number.
    # TODO: Define the priorities.
    def putCommand(self, aCommand, aPriority=100):
        self.__mCommandProcessor.put((aPriority, aCommand))

    # FIXME: A magic number.
    # TODO: Define the priorities.
    def putMessage(self, aMessage, aPriority=100):
        self.__mMessageProcessor.put((aPriority, aMessage))

    def insertRecvRequest(self, aMessageName, aCritthash, aMessage, aSoftTimeout=3, aHardTimeout=5):
        assert aCritthash not in self.mRecvReq[aMessageName], "Not handled yet. Duplicated critthash."
        self.mLogger.debug("Insert(ing) the recv request: [%s][%s]." % (aMessageName, aCritthash))
        self.mRecvReq[aMessageName][aCritthash] = {
            'message':     aMessage,
            'timestamp':   time.time(),
            'softTimeout': aSoftTimeout,
            'hardTimeout': aHardTimeout
        }

    def deleteRecvRequest(self, aMessageName, aCritthash):
        if aCritthash in self.mRecvReq[aMessageName]:
            self.mLogger.debug("Delete(ing) the recv request: [%s][%s]." % (aMessageName, aCritthash))
            del self.mRecvReq[aMessageName][aCritthash]

    def insertSentRequest(self, aMessageName, aCritthash, aMessage, aSoftTimeout=3, aHardTimeout=5):
        assert aCritthash not in self.mSentReq[aMessageName], "Not handled yet. Duplicated critthash."
        self.mLogger.debug("Insert(ing) the sent request: [%s][%s]." % (aMessageName, aCritthash))
        self.mSentReq[aMessageName][aCritthash] = {
            'message':     aMessage,
            'timestamp':   time.time(),
            'softTimeout': aSoftTimeout,
            'hardTimeout': aHardTimeout
        }
        self.mLogger.debug("Sending the %s message." % aMessageName)
        self.mPostOffice.putOutgoingAnnouncement(aMessage)

    def deleteSentRequest(self, aMessageName, aCritthash):
        if aCritthash in self.mSentReq[aMessageName]:
            self.mLogger.debug("Delete(ing) the sent request: [%s][%s]." % (aMessageName, aCritthash))
            del self.mSentReq[aMessageName][aCritthash]
