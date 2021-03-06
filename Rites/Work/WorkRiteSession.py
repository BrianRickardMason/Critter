import logging
import time
import threading

class WorkRiteSession(threading.Thread):
    def __init__(self, aRite, aGraphExecutionCritthash, aGraphName, aGraphCycle, aWorkExecutionCritthash, aWorkName, aWorkCycle):
        # Configuring the logger.
        self.mLogger = logging.getLogger(self.__class__.__name__)
        self.mLogger.propagate = False
        handler = logging.FileHandler('/tmp/' + aRite.mCritter.mCrittnick + '.log')
        formatter = logging.Formatter('[%(asctime)s][%(threadName)28s][%(levelname)8s] - %(message)s')
        handler.setFormatter(formatter)
        self.mLogger.addHandler(handler)
        self.mLogger.setLevel(aRite.mCritter.mSettings.get('logging', 'level'))

        self.mRite                    = aRite
        self.mGraphExecutionCritthash = aGraphExecutionCritthash
        self.mGraphName               = aGraphName
        self.mGraphCycle              = aGraphCycle
        self.mWorkExecutionCritthash  = aWorkExecutionCritthash
        self.mWorkName                = aWorkName
        self.mWorkCycle               = aWorkCycle

        threading.Thread.__init__(self, name='WorkRiteSession')

    def run(self):
        self.mLogger.info("Work started: %s@%s: %s@%s." % (self.mGraphName,
                                                           self.mGraphCycle,
                                                           self.mWorkName,
                                                           self.mWorkCycle))

        # FIXME: Simulate some work here.
        import random
        time.sleep(random.randint(1, 12))

        self.mLogger.info("Work ended: %s@%s: %s@%s." % (self.mGraphName,
                                                         self.mGraphCycle,
                                                         self.mWorkName,
                                                         self.mWorkCycle))

        messageNameReq = 'Command_ExecuteWork_Req'
        messageNameRes = 'Command_ExecuteWork_Res'
        message = self.mRite.mPostOffice.encode({
            'messageName':             messageNameRes,
            'graphExecutionCritthash': self.mGraphExecutionCritthash,
            'graphName':               self.mGraphName,
            'graphCycle':              self.mGraphCycle,
            'workExecutionCritthash':  self.mWorkExecutionCritthash,
            'workName':                self.mWorkName
        })
        self.mRite.deleteRecvRequest(messageNameReq, self.mWorkExecutionCritthash)
        self.mLogger.debug("Sending the %s message." % messageNameRes)
        self.mRite.mPostOffice.putOutgoingAnnouncement(message)

        # Delete myself from sessions.
        del self.mRite.mSessions[self.mWorkName][self.mWorkCycle]
