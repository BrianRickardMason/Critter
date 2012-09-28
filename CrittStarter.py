import xml.etree.ElementTree as ElementTree

from subprocess import Popen

# TODO: Discuss about the SCM side of the project.
# TODO: Discuss about the code review and quality.

# TODO: Secure it.
# TODO: Error codes!
class Crittstarter(object):
    def __init__(self):
        self.mTree = ElementTree.parse('CrittWorkPlan.xml')
        self.mRoot = self.mTree.getroot()

        self.mSettings = {}
        self.mCrittBrokerData = {}
        self.mCritterData = {}

    def start(self):
        self.__getSettings()
        self.__readCrittBrokers()
        self.__readCritters()
        self.__startCrittBrokers()
        self.__startCritters()

    def __getSettings(self):
        settings = self.mRoot.find('settings')
        self.mSettings['username'] = settings.find('username').text
        self.mSettings['workingDirectory'] = settings.find('workingDirectory').text
        self.mSettings['heartbeat'] = settings.find('heartbeat').text
        self.mSettings['maxDelay'] = settings.find('maxDelay').text

        self.mCrittBrokerData = {}

    def __readCrittBrokers(self):
        crittBrokers = self.mRoot.find('infrastructure').find('crittBrokers')

        for crittBroker in crittBrokers:
            name = crittBroker.find('name').text
            self.mCrittBrokerData[name] = {}
            self.mCrittBrokerData[name]['name'] = crittBroker.find('name').text
            self.mCrittBrokerData[name]['host'] = crittBroker.find('host').text
            # TODO: Auto-vivification.
            self.mCrittBrokerData[name]['connections'] = {}
            self.mCrittBrokerData[name]['connections']['publish'] = {}
            self.mCrittBrokerData[name]['connections']['subscribe'] = {}
            self.mCrittBrokerData[name]['connections']['ui'] = {}
            self.mCrittBrokerData[name]['connections']['brokers'] = {}
            connections = crittBroker.find('connections')
            self.mCrittBrokerData[name]['connections']['publish']['protocol'] = connections.find('publish').find('protocol').text
            self.mCrittBrokerData[name]['connections']['publish']['port'] = connections.find('publish').find('port').text
            self.mCrittBrokerData[name]['connections']['subscribe']['protocol'] = connections.find('subscribe').find('protocol').text
            self.mCrittBrokerData[name]['connections']['subscribe']['port'] = connections.find('subscribe').find('port').text
            self.mCrittBrokerData[name]['connections']['ui']['protocol'] = connections.find('ui').find('protocol').text
            self.mCrittBrokerData[name]['connections']['ui']['port'] = connections.find('ui').find('port').text

            for brokerConnection in connections.find('brokers'):
                neighbourName = brokerConnection.find('name').text
                self.mCrittBrokerData[name]['connections']['brokers'][neighbourName] = {}
                self.mCrittBrokerData[name]['connections']['brokers'][neighbourName]['publish'] = {}
                self.mCrittBrokerData[name]['connections']['brokers'][neighbourName]['subscribe'] = {}
                self.mCrittBrokerData[name]['connections']['brokers'][neighbourName]['publish']['protocol'] = brokerConnection.find('publish').find('protocol').text
                self.mCrittBrokerData[name]['connections']['brokers'][neighbourName]['publish']['port'] = brokerConnection.find('publish').find('port').text
                self.mCrittBrokerData[name]['connections']['brokers'][neighbourName]['subscribe']['protocol'] = brokerConnection.find('subscribe').find('protocol').text
                self.mCrittBrokerData[name]['connections']['brokers'][neighbourName]['subscribe']['port'] = brokerConnection.find('subscribe').find('port').text

    def __readCritters(self):
        critters = self.mRoot.find('infrastructure').find('critters')

        for critter in critters:
            crittnick = critter.find('crittnick').text
            self.mCritterData[crittnick] = {}
            self.mCritterData[crittnick]['crittnick'] = critter.find('crittnick').text
            self.mCritterData[crittnick]['host'] = critter.find('host').text
            self.mCritterData[crittnick]['crittBroker'] = critter.find('crittBroker').text
            # TODO: Naming convention: brokerName?
            brokerName = self.mCritterData[crittnick]['crittBroker']
            if brokerName in self.mCrittBrokerData:
                self.mCritterData[crittnick]['connections'] = {}
                self.mCritterData[crittnick]['connections']['publish'] = {}
                self.mCritterData[crittnick]['connections']['subscribe'] = {}
                self.mCritterData[crittnick]['connections']['publish']['protocol'] = self.mCrittBrokerData[brokerName]['connections']['subscribe']['protocol']
                self.mCritterData[crittnick]['connections']['publish']['host'] = self.mCrittBrokerData[brokerName]['host']
                self.mCritterData[crittnick]['connections']['publish']['port'] = self.mCrittBrokerData[brokerName]['connections']['subscribe']['port']
                self.mCritterData[crittnick]['connections']['subscribe']['protocol'] = self.mCrittBrokerData[brokerName]['connections']['publish']['protocol']
                self.mCritterData[crittnick]['connections']['subscribe']['host'] = self.mCrittBrokerData[brokerName]['host']
                self.mCritterData[crittnick]['connections']['subscribe']['port'] = self.mCrittBrokerData[brokerName]['connections']['publish']['port']
            else:
                # TODO: Make meaningful.
                raise Exception
            self.mCritterData[crittnick]['services'] = []
            for service in critter.find('services'):
                self.mCritterData[crittnick]['services'].append(service.text)

    def __startCrittBrokers(self):
        # TODO: Implement me!
        pass

    def __startCritters(self):
        # TODO: Implement me!
        pass

    def __startCrittBroker(self, aName):
        Popen([
            'ssh',
            'crittuser@' + self.mCrittBrokerData[aName]['host'],
            'python',
            '/home/crittuser/sandbox/Critter/CrittBroker.py',
            self.mCrittBrokerData[aName]['name'],
            self.mCrittBrokerData[aName]['host'],
            self.mCrittBrokerData[aName]['connections']['publish']['protocol'],
            self.mCrittBrokerData[aName]['connections']['publish']['port'],
            self.mCrittBrokerData[aName]['connections']['subscribe']['protocol'],
            self.mCrittBrokerData[aName]['connections']['subscribe']['port'],
            self.mCrittBrokerData[aName]['connections']['ui']['protocol'],
            self.mCrittBrokerData[aName]['connections']['ui']['port']
        ])

    def __startCritter(self, aCritterData):
        Popen([
            'ssh',
            'crittuser@' + aCritterData['host'],
            'python',
            '/home/crittuser/sandbox/Critter/CrittInit.py',
            aCritterData['crittnick'],
            aCritterData['host'],
            aCritterData['connections']['publish']['protocol'],
            aCritterData['connections']['publish']['host'],
            aCritterData['connections']['publish']['port'],
            aCritterData['connections']['subscribe']['protocol'],
            aCritterData['connections']['subscribe']['host'],
            aCritterData['connections']['subscribe']['port'],
            aCritterData['services'][0]
        ])

if __name__ == "__main__":
    crittstarter = Crittstarter()
    crittstarter.start()
