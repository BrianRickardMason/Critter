import logging

class Settings(object):
    # TODO: Error handling, e.g. missing file, invalid file, etc.
    # TODO: Pass the path to the file as a parameter. If not provided then try to read the default file.
    # TODO: Should be somehow smarter.

    def __init__(self, aBrokerPublisher, aBrokerSubscriber):
        # An empty dictionary for the beginning.
        self.mSettings = {}

        # Put the maniest into the dictionary.
        # TODO: Auto-vivification needed (?)
        self.mSettings['crittwork'] = {}
        self.mSettings['crittwork']['policy'] = 'broker' # configParser.get('crittwork', 'policy')

        # TODO: Remove me!
        self.mSettings['crittwork']['multicast'] = 'fake'

        self.mSettings['crittwork']['brokerPublisher']  = aBrokerPublisher
        self.mSettings['crittwork']['brokerSubscriber'] = aBrokerSubscriber

        self.mSettings['heartbeat'] = {}

        # TODO: Remove me!
        self.mSettings['heartbeat']['period']   = 1 # int(configParser.get('heartbeat', 'period'))
        # TODO: Remove me!
        self.mSettings['heartbeat']['maxDelay'] = 2 # int(configParser.get('heartbeat', 'maxDelay'))

        # TODO: Hardcoded for now.
        self.mSettings['logging'] = {}
        self.mSettings['logging']['level'] = logging.INFO

    def get(self, aSection, aEntry):
        if aSection in self.mSettings:
            if aEntry in self.mSettings[aSection]:
                return self.mSettings[aSection][aEntry]

        return None
