"""Database rite commands."""

import psycopg2
import sys

from Critter.CritterData import CritterData

class DatabaseCommandLoadGraphsAndWorks(object):
    """LoadGraphsAndWorks command.

    Attributes:
        mMessage: The LoadGraphAndWorkRequest.

    """

    def __init__(self, aMessage):
        """Initializes the command.

        Arguments:
            aMessage: The LoadGraphAndWorkRequest.

        """
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        """Executes the command.

        Arguments:
            aCommandProcessor: The command processor to be visited.

        """
        if aCommandProcessor.mRite.mCritter.mCritterData.mType == self.mMessage.sender.type and \
           aCommandProcessor.mRite.mCritter.mCritterData.mNick == self.mMessage.sender.nick     :
            return

        graphDictionaries           = []
        workDictionaries            = []
        workPredecessorDictionaries = []

        try:
            connection = psycopg2.connect("host='localhost' dbname='critter' user='brian' password='brianpassword'")
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

        receiverCritterData = CritterData(self.mMessage.sender.type, self.mMessage.sender.nick)

        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            'LoadGraphAndWorkResponse',
            {'messageName':      'LoadGraphAndWorkResponse',
             'sender':           {'type': aCommandProcessor.mRite.mCritterData.mType,
                                  'nick': aCommandProcessor.mRite.mCritterData.mNick},
             'receiver':         {'type': receiverCritterData.mType,
                                  'nick': receiverCritterData.mNick},
             'graphs':           graphDictionaries,
             'works':            workDictionaries,
             'workPredecessors': workPredecessorDictionaries})
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

class DatabaseCommandLoadWorkDetails(object):
    """LoadWorkDetails command.

    Attributes:
        mMessage: The LoadWorkDetailsRequest.

    """

    def __init__(self, aMessage):
        """Initializes the command.

        Arguments:
            aMessage: LoadWorkDetailsRequest.

        """
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        """Executes the command.

        Arguments:
            aCommandProcessor: The command processor to be visited.

        """
        if aCommandProcessor.mRite.mCritter.mCritterData.mType == self.mMessage.sender.type and \
           aCommandProcessor.mRite.mCritter.mCritterData.mNick == self.mMessage.sender.nick     :
            return

        workDetailsDictionaries = []

        try:
            connection = psycopg2.connect("host='localhost' dbname='critter' user='brian' password='brianpassword'")
            cursor = connection.cursor()
        except psycopg2.DatabaseError, e:
            sys.exit(1)

        cursor.execute("SELECT * FROM workDetails")
        rows = cursor.fetchall()
        for row in rows:
            workDetailsDictionaries.append({'workName': row[0],
                                            'dummy':    row[1]})

        receiverCritterData = CritterData(self.mMessage.sender.type, self.mMessage.sender.nick)

        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            'LoadWorkDetailsResponse',
            {'messageName': 'LoadWorkDetailsResponse',
             'sender':      {'type': aCommandProcessor.mRite.mCritterData.mType,
                             'nick': aCommandProcessor.mRite.mCritterData.mNick},
             'receiver':    {'type': receiverCritterData.mType,
                             'nick': receiverCritterData.mNick},
             'details':     workDetailsDictionaries})
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

class DatabaseCommand_Handle_Command_Election_Req(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        try:
            connection = psycopg2.connect("host='localhost' dbname='critter' user='brian' password='brianpassword'")
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

        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            'Command_Election_Res',
            {'messageName': 'Command_Election_Res',
             'critthash':   self.mMessage.critthash,
             'crittnick':   winnerCrittnick}
        )
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

class DatabaseCommand_Handle_Command_DetermineGraphCycle_Req(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        graphExecutionCritthash = self.mMessage.graphExecutionCritthash

        messageName = self.mMessage.messageName
        assert graphExecutionCritthash not in aCommandProcessor.mRite.mRecvReq[messageName], "Not handled yet. Duplicated critthash."
        aCommandProcessor.mLogger.debug("Insert the received request entry: [%s][%s]." % (messageName, graphExecutionCritthash))
        aCommandProcessor.mRite.mRecvReq[messageName][graphExecutionCritthash] = self.mMessage

        try:
            connection = psycopg2.connect("host='localhost' dbname='critter' user='brian' password='brianpassword'")
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

        if graphExecutionCritthash in aCommandProcessor.mRite.mRecvReq[self.mMessage.messageName]:
            aCommandProcessor.mLogger.debug("Delete the received request entry: [%s][%s]." % (self.mMessage.messageName, graphExecutionCritthash))
            del aCommandProcessor.mRite.mRecvReq[self.mMessage.messageName][graphExecutionCritthash]

        aCommandProcessor.mLogger.debug("Sending the Command_DetermineGraphCycle_Res message.")
        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            'Command_DetermineGraphCycle_Res',
            {'messageName':             'Command_DetermineGraphCycle_Res',
             'graphExecutionCritthash': graphExecutionCritthash,
             'graphName':               self.mMessage.graphName,
             'graphCycle':              cycle})
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

class DatabaseCommand_Handle_Command_DetermineWorkCycle_Req(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        workExecutionCritthash = self.mMessage.workExecutionCritthash

        messageName = self.mMessage.messageName
        assert workExecutionCritthash not in aCommandProcessor.mRite.mRecvReq[messageName], "Not handled yet. Duplicated critthash."
        aCommandProcessor.mLogger.debug("Insert the received request entry: [%s][%s]." % (messageName, workExecutionCritthash))
        aCommandProcessor.mRite.mRecvReq[messageName][workExecutionCritthash] = self.mMessage

        try:
            connection = psycopg2.connect("host='localhost' dbname='critter' user='brian' password='brianpassword'")
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

        if workExecutionCritthash in aCommandProcessor.mRite.mRecvReq[messageName]:
            aCommandProcessor.mLogger.debug("Delete the received request entry: [%s][%s]." % (messageName, workExecutionCritthash))
            del aCommandProcessor.mRite.mRecvReq[messageName][workExecutionCritthash]

        messageName = 'Command_DetermineWorkCycle_Res'
        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            messageName,
            {'messageName':             messageName,
             'graphExecutionCritthash': self.mMessage.graphExecutionCritthash,
             'graphName':               self.mMessage.graphName,
             'graphCycle':              self.mMessage.graphCycle,
             'workExecutionCritthash':  workExecutionCritthash,
             'workName':                self.mMessage.workName,
             'workCycle':               workCycle}
        )
        aCommandProcessor.mLogger.debug("Sending the %s message." % messageName)
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)
