"""The settings read from the manifest."""

import ConfigParser

class Settings(object):
    """Holds the settings read from the manifest

    Attributes:
        mSettings The dictionary of settings.

    """

    # TODO: Error handling, e.g. missing file, invalid file, etc.
    # TODO: Pass the path to the file as a parameter. If not provided then try to read the default file.
    # TODO: Should be somehow smarter.

    def __init__(self):
        """Initializes the settings."""
        # An empty dictionary for the beginning.
        self.mSettings = {}

        # Read the manifest.
        configParser = ConfigParser.RawConfigParser()
        configParser.read('Manifest')

        # Put the maniest into the dictionary.
        # TODO: Auto-vivification needed (?)
        self.mSettings['crittwork'] = {}
        self.mSettings['crittwork']['policy'] = configParser.get('crittwork', 'policy')

        self.mSettings['crittwork']['multicast'] = configParser.get('crittworkMulticast', 'multicast')

        self.mSettings['crittwork']['brokerPublisher']  = configParser.get('crittworkBroker', 'brokerPublisher')
        self.mSettings['crittwork']['brokerSubscriber'] = configParser.get('crittworkBroker', 'brokerSubscriber')

        self.mSettings['heartbeat'] = {}
        self.mSettings['heartbeat']['period']   = int(configParser.get('heartbeat', 'period'))
        self.mSettings['heartbeat']['maxDelay'] = int(configParser.get('heartbeat', 'maxDelay'))

    def get(self, aSection, aEntry):
        """Gets a specific entry of a specific section.

        Arguments:
            aSection The name of the section.
            aEntry   The name of the entry.

        Returns The value of the entry as a string, None if not found.

        """
        if aSection in self.mSettings:
            if aEntry in self.mSettings[aSection]:
                return self.mSettings[aSection][aEntry]

        return None
