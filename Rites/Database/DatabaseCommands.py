"""Database rite commands."""

import psycopg2
import sys

from Critter.CritterData import CritterData

class DatabaseCommandDetermineGraphCycle(object):
    """DetermineGraphCycle command.

    Attributes:
        mName:    The name of the command.
        mMessage: The DetermineGraphCycleRequest.

    """

    def __init__(self, aMessage):
        """Initializes the command.

        Arguments:
            aMessage: The DetermineGraphCycleRequest.

        """
        self.mName    = 'DatabaseCommandDetermineGraphCycle'
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        """Executes the command.

        Arguments:
            aCommandProcessor: The command processor to be visited.

        """
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

        receiverCritterData = CritterData(self.mMessage.sender.type, self.mMessage.sender.nick)

        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            'DetermineGraphCycleResponse',
            {'sender':    aCommandProcessor.mRite.mCritterData,
             'receiver':  receiverCritterData,
             'graphName': self.mMessage.graphName,
             'cycle':     cycle})
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

class DatabaseCommandFoo(object):
    """Foo command.

    Attributes:
        mName: The name of the command.

    """

    def __init__(self):
        """Initializes the command."""
        self.mName = "DatabaseCommandFoo"

    def execute(self, aCommandProcessor):
        """Executes the command.

        Arguments:
            aCommandProcessor: The command processor to be visited.

        """
        try:
            connection = psycopg2.connect("host='localhost' dbname='critter' user='brian' password='brianpassword'")
            cursor = connection.cursor()
        except psycopg2.DatabaseError, e:
            sys.exit(1)

        cursor.execute("SELECT * FROM graphs")
        cursor.fetchall()

class DatabaseCommandLoadGraphsAndWorks(object):
    """LoadGraphsAndWorks command.

    Attributes:
        mName:    The name of the command.
        mMessage: The LoadGraphAndWorkRequest.

    """

    def __init__(self, aMessage):
        """Initializes the command.

        Arguments:
            aMessage: The LoadGraphAndWorkRequest.

        """
        self.mName    = "DatabaseCommandLoadGraphsAndWorks"
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        """Executes the command.

        Arguments:
            aCommandProcessor: The command processor to be visited.

        """
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
            {'critterDataSender': aCommandProcessor.mRite.mCritterData,
             'critterDataReceiver': receiverCritterData,
             'graphDictionaries': graphDictionaries,
             'workDictionaries': workDictionaries,
             'workPredecessorDictionaries': workPredecessorDictionaries})
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)
