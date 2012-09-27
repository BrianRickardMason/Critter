import psycopg2
import sys

# TODO: This command should be somewhere else.
class DatabaseCommand_Handle_Command_DescribeCrittwork_Req(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        critthash = self.mMessage.critthash

        messageNameRecvReq = self.mMessage.messageName
        aCommandProcessor.mRite.insertRecvRequest(messageNameRecvReq, critthash, self.mMessage)

        messageNameRecvRes = 'Command_DescribeCrittwork_Res'
        message = aCommandProcessor.mRite.mPostOffice.encode({
            'messageName': messageNameRecvRes,
            'critthash':   critthash,
            'dummy':       'Dummy'
        })
        aCommandProcessor.mRite.deleteRecvRequest(messageNameRecvReq, critthash)
        aCommandProcessor.mLogger.debug("Sending the %s message." % messageNameRecvRes)
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(message)

class DatabaseCommand_Handle_Command_DetermineGraphCycle_Req(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        graphExecutionCritthash = self.mMessage.graphExecutionCritthash

        messageNameRecvReq = self.mMessage.messageName
        aCommandProcessor.mRite.insertRecvRequest(messageNameRecvReq, graphExecutionCritthash, self.mMessage)

        try:
            connection = psycopg2.connect("host='192.168.1.100' dbname='critter' user='crittuser' password='crittpassword'")
            cursor = connection.cursor()
        except psycopg2.DatabaseError, e:
            sys.exit(1)

        query = """
                SELECT
                    max(cycleseq)
                FROM
                    graphCycles
                WHERE
                    graphName = '%s'
                """ % (self.mMessage.graphName)
        cursor.execute(query)

        row = cursor.fetchone()
        if row[0] == None:
            cycle = 1
        else:
            cycle = row[0] + 1

        query = """
                INSERT INTO
                    graphCycles(graphName, cycleSeq)
                VALUES
                    ('%s', '%s')
                """ % (self.mMessage.graphName, cycle)
        cursor.execute(query)

        connection.commit()

        messageNameRecvRes = 'Command_DetermineGraphCycle_Res'
        message = aCommandProcessor.mRite.mPostOffice.encode({
            'messageName':             messageNameRecvRes,
            'graphExecutionCritthash': graphExecutionCritthash,
            'graphName':               self.mMessage.graphName,
            'graphCycle':              cycle
        })
        aCommandProcessor.mRite.deleteRecvRequest(messageNameRecvReq, graphExecutionCritthash)
        aCommandProcessor.mLogger.debug("Sending the %s message." % messageNameRecvRes)
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(message)

class DatabaseCommand_Handle_Command_DetermineWorkCycle_Req(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        workExecutionCritthash = self.mMessage.workExecutionCritthash

        messageNameRecvReq = self.mMessage.messageName
        aCommandProcessor.mRite.insertRecvRequest(messageNameRecvReq, workExecutionCritthash, self.mMessage)

        try:
            connection = psycopg2.connect("host='192.168.1.100' dbname='critter' user='crittuser' password='crittpassword'")
            cursor = connection.cursor()
        except psycopg2.DatabaseError, e:
            sys.exit(1)

        query = """
                SELECT
                    max(cycle)
                FROM
                    workCycles
                WHERE
                    workName = '%s'
                """ % (self.mMessage.workName)
        cursor.execute(query)

        row = cursor.fetchone()
        if row[0] == None:
            workCycle = 1
        else:
            workCycle = row[0] + 1

        query = """
                INSERT INTO
                    workCycles(workName, cycle)
                VALUES
                    ('%s', '%s')
                """ % (self.mMessage.workName, workCycle)
        cursor.execute(query)

        connection.commit()

        messageNameRecvRes = 'Command_DetermineWorkCycle_Res'
        message = aCommandProcessor.mRite.mPostOffice.encode({
            'messageName':             messageNameRecvRes,
            'graphExecutionCritthash': self.mMessage.graphExecutionCritthash,
            'graphName':               self.mMessage.graphName,
            'graphCycle':              self.mMessage.graphCycle,
            'workExecutionCritthash':  workExecutionCritthash,
            'workName':                self.mMessage.workName,
            'workCycle':               workCycle
        })
        aCommandProcessor.mRite.deleteRecvRequest(messageNameRecvReq, workExecutionCritthash)
        aCommandProcessor.mLogger.debug("Sending the %s message." % messageNameRecvRes)
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(message)

class DatabaseCommand_Handle_Command_Election_Req(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        # TODO: Register the requests!
        try:
            connection = psycopg2.connect("host='192.168.1.100' dbname='critter' user='crittuser' password='crittpassword'")
            cursor = connection.cursor()
        except psycopg2.DatabaseError, e:
            sys.exit(1)

        query = """
                SELECT
                    count(*)
                FROM
                    elections
                WHERE
                    critthash = '%s'
                """ % (self.mMessage.critthash)
        cursor.execute(query)

        row = cursor.fetchone()

        if row[0] == 0:
            query = """
                    INSERT INTO
                        elections(critthash, crittnick)
                    VALUES
                        ('%s', '%s')
                    """ % (self.mMessage.critthash, self.mMessage.crittnick)
            cursor.execute(query)
            winnerCrittnick = self.mMessage.crittnick
        else:
            query = """
                    SELECT
                        crittnick
                    FROM
                        elections
                    WHERE
                        critthash = '%s'
                    """ % (self.mMessage.critthash)
            cursor.execute(query)
            row = cursor.fetchone()
            winnerCrittnick = row[0]

        connection.commit()

        message = aCommandProcessor.mRite.mPostOffice.encode({
            'messageName': 'Command_Election_Res',
            'critthash':   self.mMessage.critthash,
            'crittnick':   winnerCrittnick
        })
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(message)

class DatabaseCommand_Handle_Command_LoadGraphAndWork_Req(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        critthash = self.mMessage.critthash
        messageNameRecvReq = self.mMessage.messageName
        aCommandProcessor.mRite.insertRecvRequest(messageNameRecvReq,
                                                  critthash,
                                                  self.mMessage,
                                                  self.mMessage.softTimeout,
                                                  self.mMessage.hardTimeout)

        graphDictionaries           = []
        workDictionaries            = []
        workPredecessorDictionaries = []

        try:
            connection = psycopg2.connect("host='192.168.1.100' dbname='critter' user='crittuser' password='crittpassword'")
            cursor = connection.cursor()
        except psycopg2.DatabaseError, e:
            sys.exit(1)

        cursor.execute("SELECT * FROM graphs")
        rows = cursor.fetchall()
        for row in rows:
            graphDictionaries.append({'graphName': row[0]})

        cursor.execute("SELECT * FROM works")
        rows = cursor.fetchall()
        for row in rows:
            workDictionaries.append({'graphName': row[0], 'workName': row[1]})

        cursor.execute("SELECT * FROM workPredecessors")
        rows = cursor.fetchall()
        for row in rows:
            workPredecessorDictionaries.append({'workName': row[0], 'predecessorWorkName': row[1]})

        messageNameRecvRes = 'Command_LoadGraphAndWork_Res'
        message = aCommandProcessor.mRite.mPostOffice.encode({
            'messageName':      messageNameRecvRes,
            'critthash':        critthash,
            'graphs':           graphDictionaries,
            'works':            workDictionaries,
            'workPredecessors': workPredecessorDictionaries
        })
        aCommandProcessor.mRite.deleteRecvRequest(messageNameRecvReq, critthash)
        aCommandProcessor.mLogger.debug("Sending the %s message." % messageNameRecvRes)
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(message)

class DatabaseCommand_Handle_Command_LoadGraphDetails_Req(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        critthash = self.mMessage.critthash
        messageNameRecvReq = self.mMessage.messageName
        aCommandProcessor.mRite.insertRecvRequest(messageNameRecvReq,
                                                  critthash,
                                                  self.mMessage,
                                                  self.mMessage.softTimeout,
                                                  self.mMessage.hardTimeout)

        graphDetailsDictionaries = []

        try:
            connection = psycopg2.connect("host='192.168.1.100' dbname='critter' user='crittuser' password='crittpassword'")
            cursor = connection.cursor()
        except psycopg2.DatabaseError, e:
            sys.exit(1)

        cursor.execute("SELECT * FROM graphDetails")
        rows = cursor.fetchall()
        for row in rows:
            graphDetailsDictionaries.append({'graphName':   row[0],
                                             'softTimeout': row[1],
                                             'hardTimeout': row[2]})

        messageNameRecvRes = 'Command_LoadGraphDetails_Res'
        message = aCommandProcessor.mRite.mPostOffice.encode({
            'messageName':  messageNameRecvRes,
            'critthash':    critthash,
            'graphDetails': graphDetailsDictionaries
        })
        aCommandProcessor.mRite.deleteRecvRequest(messageNameRecvReq, critthash)
        aCommandProcessor.mLogger.debug("Sending the %s message." % messageNameRecvRes)
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(message)

class DatabaseCommand_Handle_Command_LoadWorkDetails_Req(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        critthash = self.mMessage.critthash
        messageNameRecvReq = self.mMessage.messageName
        aCommandProcessor.mRite.insertRecvRequest(messageNameRecvReq,
                                                  critthash,
                                                  self.mMessage,
                                                  self.mMessage.softTimeout,
                                                  self.mMessage.hardTimeout)

        workDetailsDictionaries = []

        try:
            connection = psycopg2.connect("host='192.168.1.100' dbname='critter' user='crittuser' password='crittpassword'")
            cursor = connection.cursor()
        except psycopg2.DatabaseError, e:
            sys.exit(1)

        cursor.execute("SELECT * FROM workDetails")
        rows = cursor.fetchall()
        for row in rows:
            workDetailsDictionaries.append({'workName':    row[0],
                                            'softTimeout': row[1],
                                            'hardTimeout': row[2],
                                            'dummy':       row[3]})

        messageNameRecvRes = 'Command_LoadWorkDetails_Res'
        message = aCommandProcessor.mRite.mPostOffice.encode({
            'messageName':  messageNameRecvRes,
            'critthash':    critthash,
            'workDetails':  workDetailsDictionaries
        })
        aCommandProcessor.mRite.deleteRecvRequest(messageNameRecvReq, critthash)
        aCommandProcessor.mLogger.debug("Sending the %s message." % messageNameRecvRes)
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(message)
