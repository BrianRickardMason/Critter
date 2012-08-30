"""Database rite commands."""

import psycopg2
import sys

from Critter.CritterData import CritterData

class DatabaseCommandDetermineWorkCycle(object):
    """DetermineWorkCycle command.

    Attributes:
        mMessage: The DetermineWorkCycleRequest.

    """

    def __init__(self, aMessage):
        """Initializes the command.

        Arguments:
            aMessage: The DetermineWorkCycleRequest.

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

class DatabaseCommand_Handle_Command_Req_Election(object):
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
            'Command_Res_Election',
            {'messageName': 'Command_Res_Election',
             'critthash':   self.mMessage.critthash,
             'crittnick':   winnerCrittnick}
        )
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)

class DatabaseCommand_Handle_Command_Req_DetermineGraphCycle(object):
    def __init__(self, aMessage):
        self.mMessage = aMessage

    def execute(self, aCommandProcessor):
        critthash = self.mMessage.critthash

        assert self.mMessage.messageName in aCommandProcessor.mRite.mRecvReq, "Missing key in the dictionary of received requests."
        assert critthash not in aCommandProcessor.mRite.mRecvReq[self.mMessage.messageName], "Not handled yet. Duplicated critthash."
        aCommandProcessor.mLogger.debug("Insert the received request entry: [%s][%s]." % (self.mMessage.messageName, critthash))
        aCommandProcessor.mRite.mRecvReq[self.mMessage.messageName][critthash] = True

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

        assert self.mMessage.messageName in aCommandProcessor.mRite.mRecvReq, "Missing key in the dictionary of received requests."
        if critthash in aCommandProcessor.mRite.mRecvReq[self.mMessage.messageName]:
            aCommandProcessor.mLogger.debug("Delete the received request entry: [%s][%s]." % (self.mMessage.messageName, critthash))
            del aCommandProcessor.mRite.mRecvReq[self.mMessage.messageName][critthash]

        aCommandProcessor.mLogger.debug("Sending the Command_Res_DetermineGraphCycle message.")
        envelope = aCommandProcessor.mRite.mPostOffice.encode(
            'Command_Res_DetermineGraphCycle',
            {'messageName': 'Command_Res_DetermineGraphCycle',
             'critthash':   critthash,
             'cycle':       cycle})
        aCommandProcessor.mRite.mPostOffice.putOutgoingAnnouncement(envelope)
