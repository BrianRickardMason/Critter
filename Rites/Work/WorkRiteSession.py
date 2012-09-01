import logging
import time
import threading

logging.basicConfig(format='[%(asctime)s][%(threadName)28s][%(levelname)8s] - %(message)s')

class WorkRiteSession(threading.Thread):
    def __init__(self, aRite, aGraphExecutionCritthash, aGraphName, aGraphCycle, aWorkExecutionCritthash, aWorkName, aWorkCycle):
        self.mLogger = logging.getLogger('WorkRiteSession')
        self.mLogger.setLevel(logging.INFO)

        self.mRite                    = aRite
        self.mGraphExecutionCritthash = aGraphExecutionCritthash
        self.mGraphName               = aGraphName
        self.mGraphCycle              = aGraphCycle
        self.mWorkExecutionCritthash  = aWorkExecutionCritthash
        self.mWorkName                = aWorkName
        self.mWorkCycle               = aWorkCycle

        threading.Thread.__init__(self, name='WorkRiteSession')

    def run(self):
        # TODO: Start from here.
        return

        """Starts the main flow of the session."""
        self.mLogger.info("Work started: %s@%s: %s@%s." % (self.mGraphName,
                                                           self.mGraphCycle,
                                                           self.mWorkName,
                                                           self.mWorkCycle))

        # FIXME: Simulate some work here.
        import random
        time.sleep(random.randint(1, 12))

        # Succeed.
        if random.randint(0, 90) > 100:
            result = True
        # Failed.
        else:
            result = False

        # Report finished work.
        envelope = self.mRite.mPostOffice.encode(
            'ReportFinishedWorkAnnouncement',
            {'messageName': 'ReportFinishedWorkAnnouncement',
             'sender':      {'type': self.mRite.mCritterData.mType,
                             'nick': self.mRite.mCritterData.mNick},
             'graphName':   self.mGraphName,
             'graphCycle':  self.mGraphCycle,
             'workName':    self.mWorkName,
             'workCycle':   self.mWorkCycle,
             'result':      result})
        self.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

        self.mLogger.info("Work ended: %s@%s: %s@%s." % (self.mGraphName,
                                                         self.mGraphCycle,
                                                         self.mWorkName,
                                                         self.mWorkCycle))

        # Delete myself from sessions.
        del self.mRite.mSessions[self.mWorkName][self.mWorkCycle]
