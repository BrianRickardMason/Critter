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
            {'messageName': 'DetermineGraphCycleResponse',
             'sender':      {'type': aCommandProcessor.mRite.mCritterData.mType,
                             'nick': aCommandProcessor.mRite.mCritterData.mNick},
             'receiver':    {'type': receiverCritterData.mType,
                             'nick': receiverCritterData.mNick},
             'graphName':   self.mMessage.graphName,
             'cycle':       cycle})
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

class DatabaseCommandDetermineWorkCycle(object):
    """DetermineWorkCycle command.

    Attributes:
        mName:    The name of the command.
        mMessage: The DetermineWorkCycleRequest.

    """

    def __init__(self, aMessage):
        """Initializes the command.

        Arguments:
            aMessage: The DetermineWorkCycleRequest.

        """
        self.mName    = 'DatabaseCommandDetermineWorkCycle'
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
                    max(cycle)
                FROM
                    workCycles
                WHERE
                    workName = '%s'
                """ % (self.mMessage.workName)
        cursor.execute(query)

        row = cursor.fetchone()
        if row[0] == None:
            cycle = 1
        else:
            cycle = row[0] + 1

        query = """
                INSERT INTO
                    workCycles(workName, cycle)
                VALUES
                    ('%s', '%s')
                """ % (self.mMessage.workName, cycle)
        cursor.execute(query)

        connection.commit()

        receiverCritterData = CritterData(self.mMessage.sender.type, self.mMessage.sender.nick)

        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            'DetermineWorkCycleResponse',
            {'messageName': 'DetermineWorkCycleResponse',
             'sender':      {'type': aCommandProcessor.mRite.mCritterData.mType,
                             'nick': aCommandProcessor.mRite.mCritterData.mNick},
             'receiver':    {'type': receiverCritterData.mType,
                             'nick': receiverCritterData.mNick},
             'graphName':   self.mMessage.graphName,
             'cycle':       self.mMessage.cycle,
             'workName':    self.mMessage.workName,
             'workCycle':   cycle})
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

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
            {'messageName':      'LoadGraphAndWorkResponse',
             'sender':           {'type': aCommandProcessor.mRite.mCritterData.mType,
                                  'nick': aCommandProcessor.mRite.mCritterData.mNick},
             'receiver':         {'type': receiverCritterData.mType,
                                  'nick': receiverCritterData.mNick},
             'graphs':           graphDictionaries,
             'works':            workDictionaries,
             'workPredecessors': workPredecessorDictionaries})
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)
