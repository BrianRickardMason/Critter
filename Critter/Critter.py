"""The Critter - the base for other critters."""

import logging
import sys
import time

import Rites.RiteCommon

from CritterBehavior       import CritterBehavior
from PostOffice.PostOffice import PostOffice
from Rites.RiteFactory     import createRite
from Settings              import Settings

logging.basicConfig(format='[%(asctime)s][%(threadName)28s][%(levelname)8s] - %(message)s')

class Critter(object):
    """The Critter - the base for other critters.

    All other critters written in python should derive from this class.

    Attributes:
        mBehavior:         The behavior.
        mGracefulShutdown: Defines whether the graceful shutdown was not started.
        mLogger:           The logger.
        mPostOffice:       The post office that handles all communication.
        mRites:            The dictionary of rites.
        mSettings:         The settings read from the manifest.
        mCrittnick:        The crittnick.

    """

    # TODO: Remove aType.
    def __init__(self, aType, aNick, aRites):
        """Initializes the critter.

        Arguments:
            aType:  The type of the critter.
            aNick:  The nick of the critter.
            aRites: The rites to be started (specific ones).

        """
        self.mSettings = Settings()

        self.mLogger = logging.getLogger(aType)
        self.mLogger.setLevel(self.mSettings.get('logging', 'level'))

        self.mCrittnick = aNick

        # TODO: Implement sequential starting (in order of dependencies).
        #       This is a matter of performing full startup procedure properly.
        self.mRites = {}

        self.mLogger.debug("Initializing the post office.")
        self.mPostOffice = PostOffice(self)

        self.mGracefulShutdown = False

        # FIXME: Rites should be started in appropriate sequence, according to dependencies.
        rites = [Rites.RiteCommon.REGISTRY, Rites.RiteCommon.HEARTBEAT] + aRites
        for rite in rites:
            self.mLogger.info("Spawning the %s rite." % rite)
            if rite in self.mRites:
                # TODO: For now this is ok. If e.g. rites are started recursively, then this will not work!
                self.mLogger.critical("Rite %s has been already started." % rite)
                sys.exit(1)
            else:
                self.mRites[rite] = createRite(self, rite)

        for rite in rites:
            self.mLogger.info("Starting the %s rite." % rite)
            self.mRites[rite].start()

        # Spawning the behavior.
        self.mLogger.debug("Spawning the behavior.")
        self.mBehavior = CritterBehavior(self)
        self.mBehavior.setDaemon(True)
        self.mBehavior.start()

        self.mLogger.debug("Starting the post office.")
        self.mPostOffice.start()

    def run(self):
        """Runs the critter."""
        self.mLogger.debug("Critter is alive and kicking. And starts to run...")

        while not self.mGracefulShutdown:
            self.mLogger.debug("Sleeping for a heartbeat.")
            time.sleep(self.mSettings.get('heartbeat', 'period'))

        self.mLogger.debug("Goodbye, cruel world...")

    def getPostOffice(self):
        """Gets the post office that handles all communication.

        Returns:
            The post office that handles all communication.

        """
        return self.mPostOffice

    def getSettings(self):
        """Gets the critter's settings (read from the manifest).

        Returns:
            The critter's settings (read from the manifest).
        """
        return self.mSettings
