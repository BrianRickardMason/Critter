import logging
import threading

from Rites.CommandProcessor import CommandProcessor

logging.basicConfig(format='[%(asctime)s][%(threadName)28s][%(levelname)8s] - %(message)s')

class Rite(threading.Thread):
    def __init__(self, aCritter, aSettings, aPostOffice, aRiteName, aMessageProcessorType):
        self.mSettings = aSettings

        self.mLogger = logging.getLogger(aRiteName + 'Rite')
        self.mLogger.setLevel(self.mSettings.get('logging', 'level'))

        self.mCritter     = aCritter
        self.mPostOffice  = aPostOffice
        self.mRiteName    = aRiteName

        self.mLogger.info("Spawning the command processor.")
        self.mCommandProcessor = CommandProcessor(self)
        self.mCommandProcessor.setDaemon(True)
        self.mCommandProcessor.start()

        self.mLogger.info("Spawning the message processor.")
        self.mMessageProcessor = aMessageProcessorType(self)
        self.mMessageProcessor.setDaemon(True)
        self.mMessageProcessor.start()

        threading.Thread.__init__(self, name=aRiteName + 'Rite')

    def run(self):
        raise NotImplementedError

    def putCommand(self, aCommand):
        self.mCommandProcessor.put(aCommand)

    def putMessage(self, aMessage):
        self.mMessageProcessor.put(aMessage)

    def insertRecvRequest(self, aMessageName, aCritthash, aMessage, aSoftTimeout=3, aHardTimeout=5):
        assert aCritthash not in self.mRecvReq[aMessageName], "Not handled yet. Duplicated critthash."
        self.mLogger.debug("Insert(ing) the recv request: [%s][%s]." % (aMessageName, aCritthash))
        self.mRecvReq[aMessageName][aCritthash] = aMessage

    def deleteRecvRequest(self, aMessageName, aCritthash):
        if aCritthash in self.mRecvReq[aMessageName]:
            self.mLogger.debug("Delete(ing) the recv request: [%s][%s]." % (aMessageName, aCritthash))
            del self.mRecvReq[aMessageName][aCritthash]

    def insertSentRequest(self, aMessageName, aCritthash, aEnvelope, aSoftTimeout=3, aHardTimeout=5):
        assert aCritthash not in self.mSentReq[aMessageName], "Not handled yet. Duplicated critthash."
        self.mLogger.debug("Insert(ing) the sent request: [%s][%s]." % (aMessageName, aCritthash))
        self.mSentReq[aMessageName][aCritthash] = {
            'envelope':    aEnvelope,
            'softTimeout': aSoftTimeout,
            'hardTimeout': aHardTimeout
        }
        self.mLogger.debug("Sending the %s message." % aMessageName)
        self.mPostOffice.putOutgoingAnnouncement(aEnvelope)

    def deleteSentRequest(self, aMessageName, aCritthash):
        if aCritthash in self.mSentReq[aMessageName]:
            self.mLogger.debug("Delete(ing) the sent request: [%s][%s]." % (aMessageName, aCritthash))
            del self.mSentReq[aMessageName][aCritthash]
