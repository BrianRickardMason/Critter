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

    def start(self):
        self.__getSettings()
        self.__startCrittBrokers()
        self.__startCritters()

    def __getSettings(self):
        settings = self.mRoot.find('settings')
        self.mSettings['username'] = settings.find('username').text
        self.mSettings['workingDirectory'] = settings.find('workingDirectory').text
        self.mSettings['heartbeat'] = settings.find('heartbeat').text
        self.mSettings['maxDelay'] = settings.find('maxDelay').text

        self.mCrittBrokerData = {}

    def __startCrittBrokers(self):
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
            connections = crittBroker.find('connections')
            self.mCrittBrokerData[name]['connections']['publish']['protocol'] = connections.find('publish').find('protocol').text
            self.mCrittBrokerData[name]['connections']['publish']['port'] = connections.find('publish').find('port').text
            self.mCrittBrokerData[name]['connections']['subscribe']['protocol'] = connections.find('subscribe').find('protocol').text
            self.mCrittBrokerData[name]['connections']['subscribe']['port'] = connections.find('subscribe').find('port').text
            self.mCrittBrokerData[name]['connections']['ui']['protocol'] = connections.find('ui').find('protocol').text
            self.mCrittBrokerData[name]['connections']['ui']['port'] = connections.find('ui').find('port').text

            self.__startCrittBroker(name)

    def __startCritters(self):
        critters = self.mRoot.find('infrastructure').find('critters')

        for critter in critters:
            critterData = {}

            critterData['crittnick'] = critter.find('crittnick').text
            critterData['host'] = critter.find('host').text
            critterData['crittBroker'] = critter.find('crittBroker').text
            name = critterData['crittBroker']
            if name in self.mCrittBrokerData:
                critterData['connections'] = {}
                critterData['connections']['publish'] = {}
                critterData['connections']['subscribe'] = {}
                critterData['connections']['publish']['protocol'] = self.mCrittBrokerData[name]['connections']['subscribe']['protocol']
                critterData['connections']['publish']['host'] = self.mCrittBrokerData[name]['host']
                critterData['connections']['publish']['port'] = self.mCrittBrokerData[name]['connections']['subscribe']['port']
                critterData['connections']['subscribe']['protocol'] = self.mCrittBrokerData[name]['connections']['publish']['protocol']
                critterData['connections']['subscribe']['host'] = self.mCrittBrokerData[name]['host']
                critterData['connections']['subscribe']['port'] = self.mCrittBrokerData[name]['connections']['publish']['port']
            else:
                # TODO: Make meaningful.
                raise Exception
            critterData['services'] = []
            for service in critter.find('services'):
                critterData['services'].append(service.text)

            self.__startCritter(critterData)

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
            'crittuser@' + self.aCritterData['host'],
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
