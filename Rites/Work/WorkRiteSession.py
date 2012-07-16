"""The WorkRiteSession.

Handles a full, single work execution from the beginning to the end.

"""

import logging
import time
import threading

logging.basicConfig(format='[%(asctime)s][%(threadName)28s][%(levelname)8s] - %(message)s')

class WorkRiteSession(threading.Thread):
    """The message processor of the a rite.

    Attributes:
        mLogger:     The logger.
        mRite:       The rite.
        mGraphName:  The graph name.
        mGraphCycle: The cycle number.
        mWorkName:   The work name.
        mWorkCycle:  The work cycle.

    """

    def __init__(self, aRite, aGraphName, aGraphCycle, aWorkName, aWorkCycle):
        """Initializes the message processor.

        Arguments:
            aRite:       The rite.
            aGraphName:  The graph name.
            aGraphCycle: The graph cycle.
            aWorkName:   The work name.
            aWorkCycle:  The work cycle.

        """
        self.mLogger = logging.getLogger('WorkRiteSession')
        self.mLogger.setLevel(logging.INFO)

        self.mRite       = aRite
        self.mGraphName  = aGraphName
        self.mGraphCycle = aGraphCycle
        self.mWorkName   = aWorkName
        self.mWorkCycle  = aWorkCycle

        threading.Thread.__init__(self, name='WorkRiteSession')

    def run(self):
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
            {'sender':     self.mRite.mCritterData,
             'graphName':  self.mGraphName,
             'graphCycle': self.mGraphCycle,
             'workName':   self.mWorkName,
             'workCycle':  self.mWorkCycle,
             'result':     result})
        self.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

        self.mLogger.info("Work ended: %s@%s: %s@%s." % (self.mGraphName,
                                                         self.mGraphCycle,
                                                         self.mWorkName,
                                                         self.mWorkCycle))

        # Delete myself from sessions.
        del self.mRite.mSessions[self.mWorkName][self.mWorkCycle]
