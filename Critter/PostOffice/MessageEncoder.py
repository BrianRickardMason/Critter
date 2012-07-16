"""The message encoder."""

import sys

import Messages_pb2

from MessageCommon import *

# TODO: Pass dictionaries to private functions (instead of parameters).

class MessageEncoder(object):
    """The message encoder delivers a message encoded in protobuf based upon delivered parameters.

    For all messages the parameters are taken, and an envelope is returned.

    """

    def encode(self, aMessageName, aData):
        """A method needed to have one interface for creating messages everywhere.

        Arguments:
            aMessageName: The name of the message.
            aData:        The dictionary of parameters.

        Returns:
            A message in envelope.

        """
        try:
            if aMessageName == 'CommandWorkExecutionAnnouncement':
                return self.__commandWorkExecutionAnnouncement(aData['sender'],
                                                               aData['graphName'],
                                                               aData['cycle'],
                                                               aData['workName'])

            elif aMessageName == 'DetermineGraphCycleRequest':
                return self.__determineGraphCycleRequest(aData['sender'], aData['graphName'])

            elif aMessageName == 'DetermineGraphCycleResponse':
                return self.__determineGraphCycleResponse(aData['sender'],
                                                          aData['receiver'],
                                                          aData['graphName'],
                                                          aData['cycle'])

            elif aMessageName == 'DetermineWorkCycleRequest':
                return self.__determineWorkCycleRequest(aData['sender'],
                                                        aData['graphName'],
                                                        aData['cycle'],
                                                        aData['workName'])

            elif aMessageName == 'DetermineWorkCycleResponse':
                return self.__determineWorkCycleResponse(aData['sender'],
                                                         aData['receiver'],
                                                         aData['graphName'],
                                                         aData['cycle'],
                                                         aData['workName'],
                                                         aData['workCycle'])

            elif aMessageName == 'ExecuteGraphAnnouncement':
                return self.__executeGraphAnnouncement(aData['critterData'], aData['graphName'])

            elif aMessageName == 'ExecuteWorkAnnouncement':
                return self.__executeWorkAnnouncement(aData['sender'],
                                                      aData['receiver'],
                                                      aData['graphName'],
                                                      aData['cycle'],
                                                      aData['workName'])

            elif aMessageName == 'HeartbeatAnnouncement':
                return self.__heartbeatAnnouncement(aData['critterData'], aData['timestamp'])

            elif aMessageName == 'LoadGraphAndWorkRequest':
                return self.__loadGraphAndWorkRequest(aData['critterData'])

            elif aMessageName == 'LoadGraphAndWorkResponse':
                return self.__loadGraphAndWorkResponse(aData['critterDataSender'],
                                                       aData['critterDataReceiver'],
                                                       aData['graphDictionaries'],
                                                       aData['workDictionaries'],
                                                       aData['workPredecessorDictionaries'])

            elif aMessageName == 'PokeAnnouncement':
                return self.__pokeAnnouncement(aData['critterData'])

            elif aMessageName == 'PresentYourselfRequest':
                return self.__presentYourselfRequest(aData['critterDataSender'], aData['critterDataReceiver'])

            elif aMessageName == 'PresentYourselfResponse':
                return self.__presentYourselfResponse(aData['critterDataSender'], aData['critterDataReceiver'])

            elif aMessageName == 'ReportFinishedWorkAnnouncement':
                return self.__reportFinishedWorkAnnouncement(aData['sender'],
                                                             aData['graphName'],
                                                             aData['graphCycle'],
                                                             aData['workName'],
                                                             aData['workCycle'],
                                                             aData['result'])

            else:
                # TODO: Handle this more gracefully
                print "Invalid message."
                sys.exit(1)

        except KeyError, e:
            # TODO: Handle this more gracefully
            print e
            sys.exit(1)

    def __commandWorkExecutionAnnouncement(self, aSender, aGraphName, aCycle, aWorkName):
        """Encodes CommandWorkExecutionAnnouncement.

        Arguments:
            aSender:    The critter data of sender.
            aReceiver:  The critter data of receiver.
            aGraphName: The name of the graph.
            aCycle:     The cycle of the graph.
            aWorkName:  The name of the work.

        Returns:
            CommandWorkExecutionAnnouncement envelope.

        """
        payload = Messages_pb2.CommandWorkExecutionAnnouncement()
        payload.messageName = 'CommandWorkExecutionAnnouncement'
        payload.sender.type = aSender.mType
        payload.sender.nick = aSender.mNick
        payload.graphName   = aGraphName
        payload.cycle       = aCycle
        payload.workName    = aWorkName

        return self.__putIntoAnEnvelope(COMMAND_WORK_EXECUTION_ANNOUNCEMENT, payload)

    def __determineGraphCycleRequest(self, aSender, aGraphName):
        """Encodes DetermineGraphCycleRequest.

        Arguments:
            aSender:    The critter data of sender.
            aGraphName: The name of the graph.

        Returns:
            DetermineGraphCycleRequest envelope.

        """
        payload = Messages_pb2.DetermineGraphCycleRequest()
        payload.messageName = 'DetermineGraphCycleRequest'
        payload.sender.type = aSender.mType
        payload.sender.nick = aSender.mNick
        payload.graphName   = aGraphName

        return self.__putIntoAnEnvelope(DETERMINE_GRAPH_CYCLE_REQUEST, payload)

    def __determineGraphCycleResponse(self, aSender, aReceiver, aGraphName, aCycle):
        """Encodes DetermineGraphCycleRequest.

        Arguments:
            aSender:    The critter data of sender.
            aReceiver:  The critter data of receiver.
            aGraphName: The name of the graph.
            aCycle:     The cycle of the graph.

        Returns:
            DetermineGraphCycleResponse envelope.

        """
        payload = Messages_pb2.DetermineGraphCycleResponse()
        payload.messageName   = 'DetermineGraphCycleResponse'
        payload.sender.type   = aSender.mType
        payload.sender.nick   = aSender.mNick
        payload.receiver.type = aReceiver.mType
        payload.receiver.nick = aReceiver.mNick
        payload.graphName     = aGraphName
        payload.cycle         = aCycle

        return self.__putIntoAnEnvelope(DETERMINE_GRAPH_CYCLE_RESPONSE, payload)

    def __determineWorkCycleRequest(self, aSender, aGraphName, aCycle, aWorkName):
        """Encodes DetermineWorkCycleRequest.

        Arguments:
            aSender:    The critter data of sender.
            aGraphName: The name of the graph.
            aCycle:     The cycle of the graph.
            aWorkName:  The name of the work.

        Returns:
            DetermineWorkCycleRequest envelope.

        """
        payload = Messages_pb2.DetermineWorkCycleRequest()
        payload.messageName = 'DetermineWorkCycleRequest'
        payload.sender.type = aSender.mType
        payload.sender.nick = aSender.mNick
        payload.graphName   = aGraphName
        payload.cycle       = aCycle
        payload.workName    = aWorkName

        return self.__putIntoAnEnvelope(DETERMINE_WORK_CYCLE_REQUEST, payload)

    def __determineWorkCycleResponse(self, aSender, aReceiver, aGraphName, aCycle, aWorkName, aWorkCycle):
        """Encodes DetermineWorkCycleResponse.

        Arguments:
            aSender:    The critter data of sender.
            aReceiver:  The critter data of receiver.
            aGraphName: The name of the graph.
            aCycle:     The cycle of the graph.
            aWorkName:  The name of the work.
            aWorkCycle: The cycle of the work.

        Returns:
            DetermineWorkCycleResponse envelope.

        """
        payload = Messages_pb2.DetermineWorkCycleResponse()
        payload.messageName   = 'DetermineWorkCycleResponse'
        payload.sender.type   = aSender.mType
        payload.sender.nick   = aSender.mNick
        payload.receiver.type = aReceiver.mType
        payload.receiver.nick = aReceiver.mNick
        payload.graphName     = aGraphName
        payload.cycle         = aCycle
        payload.workName      = aWorkName
        payload.workCycle     = aWorkCycle

        return self.__putIntoAnEnvelope(DETERMINE_WORK_CYCLE_RESPONSE, payload)

    def __executeGraphAnnouncement(self, aCritterData, aGraphName):
        """Encodes ExecuteGraphAnnouncement.

        Arguments:
            aCritterData: The critter data.
            aGraphName:   The name of the graph.

        Returns:
            ExecuteGraphAnnouncement envelope.

        """
        payload = Messages_pb2.ExecuteGraphAnnouncement()
        payload.messageName = 'ExecuteGraphAnnouncement'
        payload.sender.type = aCritterData.mType
        payload.sender.nick = aCritterData.mNick
        payload.graphName   = aGraphName

        return self.__putIntoAnEnvelope(EXECUTE_GRAPH_ANNOUNCEMENT, payload)

    def __executeWorkAnnouncement(self, aSender, aReceiver, aGraphName, aCycle, aWorkName):
        """Encodes ExecuteWorkAnnouncement.

        Arguments:
            aSender:    The critter data of sender.
            aReceiver:  The critter data of receiver.
            aGraphName: The name of the graph.
            aCycle:     The cycle of the graph.
            aWorkName:  The name of the work.

        Returns:
            ExecuteWorkAnnouncement envelope.

        """
        payload = Messages_pb2.ExecuteWorkAnnouncement()
        payload.messageName   = 'ExecuteWorkAnnouncement'
        payload.sender.type   = aSender.mType
        payload.sender.nick   = aSender.mNick
        payload.receiver.type = aReceiver.mType
        payload.receiver.nick = aReceiver.mNick
        payload.graphName     = aGraphName
        payload.cycle         = aCycle
        payload.workName      = aWorkName

        return self.__putIntoAnEnvelope(EXECUTE_WORK_ANNOUNCEMENT, payload)

    def __heartbeatAnnouncement(self, aCritterData, aTimestamp):
        """Encodes HeartbeatAnnouncement.

        Arguments:
            aCritterData The critter data.
            aTimestamp   The timestamp.

        Returns HeartbeatAnnouncement envelope.

        """
        payload = Messages_pb2.HeartbeatAnnouncement()
        payload.messageName = 'HeartbeatAnnouncement'
        payload.sender.type = aCritterData.mType
        payload.sender.nick = aCritterData.mNick
        payload.timestamp   = aTimestamp

        return self.__putIntoAnEnvelope(HEARTBEAT_ANNOUNCEMENT, payload)

    def __loadGraphAndWorkRequest(self, aCritterData):
        """Encodes LoadGraphAndWorkRequest.

        Arguments:
            aCritterData: The critter data.

        Returns:
            LoadGraphAndWorkRequest envelope.

        """
        payload = Messages_pb2.LoadGraphAndWorkRequest()
        payload.messageName = 'LoadGraphAndWorkRequest'
        payload.sender.type = aCritterData.mType
        payload.sender.nick = aCritterData.mNick

        return self.__putIntoAnEnvelope(LOAD_GRAPH_AND_WORK_REQUEST, payload)

    def __loadGraphAndWorkResponse(self,
                                   aCritterDataSender,
                                   aCritterDataReceiver,
                                   aGraphDictionaries,
                                   aWorkDictionaries,
                                   aWorkPredecessorDictionaries):
        """Encodes LoadGraphAndWorkResponse.

        Arguments:
            aCritterDataSender:           The critter data of the sender.
            aCritterDataReceiver:         The critter data of the receiver.
            aGraphDictionaries:           The dictionaries of graph data.
            aWorkDictionaries:            The dictionaries of work data.
            aWorkPredecessorDictionaries: The dictionaries of work predecessors data.

        Returns:
            LoadGraphAndWorkResponse envelope.

        """
        payload = Messages_pb2.LoadGraphAndWorkResponse()
        payload.messageName   = 'LoadGraphAndWorkResponse'
        payload.sender.type   = aCritterDataSender.mType
        payload.sender.nick   = aCritterDataSender.mNick
        payload.receiver.type = aCritterDataReceiver.mType
        payload.receiver.nick = aCritterDataReceiver.mNick

        for graphDictionary in aGraphDictionaries:
            graphData = Messages_pb2.GraphData()
            graphData.graphName = graphDictionary['graphName']
            payload.graphs.extend([graphData])

        for workDictionary in aWorkDictionaries:
            workData = Messages_pb2.WorkData()
            workData.graphName = workDictionary['graphName']
            workData.workName = workDictionary['workName']
            payload.works.extend([workData])

        for workPredecessorDictionary in aWorkPredecessorDictionaries:
            workPredecessorData = Messages_pb2.WorkPredecessorData()
            workPredecessorData.workName = workPredecessorDictionary['workName']
            workPredecessorData.predecessorWorkName = workPredecessorDictionary['predecessorWorkName']
            payload.workPredecessors.extend([workPredecessorData])

        return self.__putIntoAnEnvelope(LOAD_GRAPH_AND_WORK_RESPONSE, payload)

    def __pokeAnnouncement(self, aCritterData):
        """Encodes PokeAnnouncement.

        Arguments:
            aCritterData: The critter data.

        Returns PokeAnnouncement envelope.

        """
        payload = Messages_pb2.PokeAnnouncement()
        payload.messageName = 'PokeAnnouncement'
        payload.sender.type = aCritterData.mType
        payload.sender.nick = aCritterData.mNick

        return self.__putIntoAnEnvelope(POKE_ANNOUNCEMENT, payload)

    def __presentYourselfRequest(self, aCritterDataSender, aCritterDataReceiver):
        """Encodes PresentYourselfRequest.

        Arguments:
            aCritterDataSender:   The critter data of the sender.
            aCritterDataReceiver: The critter data of the receiver.

        Returns PresentYourselfRequest envelope.

        """
        payload = Messages_pb2.PresentYourselfRequest()
        payload.messageName   = 'PresentYourselfRequest'
        payload.sender.type   = aCritterDataSender.mType
        payload.sender.nick   = aCritterDataSender.mNick
        payload.receiver.type = aCritterDataReceiver.mType
        payload.receiver.nick = aCritterDataReceiver.mNick

        return self.__putIntoAnEnvelope(PRESENT_YOURSELF_REQUEST, payload)

    def __presentYourselfResponse(self, aCritterDataSender, aCritterDataReceiver):
        """Encodes PresentYourselfResponse.

        Arguments:
            aCritterDataSender:   The critter data of the sender.
            aCritterDataReceiver: The critter data of the receiver.

        Returns PresentYourselfResponse envelope.

        """
        payload = Messages_pb2.PresentYourselfResponse()
        payload.messageName   = 'PresentYourselfResponse'
        payload.sender.type   = aCritterDataSender.mType
        payload.sender.nick   = aCritterDataSender.mNick
        payload.receiver.type = aCritterDataReceiver.mType
        payload.receiver.nick = aCritterDataReceiver.mNick

        return self.__putIntoAnEnvelope(PRESENT_YOURSELF_RESPONSE, payload)

    def __reportFinishedWorkAnnouncement(self, aSender, aGraphName, aGraphCycle, aWorkName, aWorkCycle, aResult):
        """Encodes ReportFinishedWorkAnnouncement

        Arguments:
            aSender:     The critter data of sender.
            aGraphName:  The graph name.
            aGraphCycle: The graph cycle.
            aWorkName:   The work name.
            aWorkCycle:  The work cycle.

        Returns:
            ReportFinishedWorkAnnouncement envelope.

        """
        payload = Messages_pb2.ReportFinishedWorkAnnouncement()
        payload.messageName = 'ReportFinishedWorkAnnouncement'
        payload.sender.type = aSender.mType
        payload.sender.nick = aSender.mNick
        payload.graphName   = aGraphName
        payload.graphCycle  = aGraphCycle
        payload.workName    = aWorkName
        payload.workCycle   = aWorkCycle
        payload.result      = aResult

        return self.__putIntoAnEnvelope(REPORT_FINISHED_WORK_ANNOUNCEMENT, payload)

    def __putIntoAnEnvelope(self, aId, aPayload):
        """Puts the payload into an envelope.

        Arguments:
            aId      The id of a header.
            aPayload The payload.

        Returns The envelope.

        """
        envelope = Messages_pb2.Envelope()
        envelope.header.id       = aId
        envelope.payload.payload = aPayload.SerializeToString()

        return envelope
