"""The message encoder."""

import sys

import Messages_pb2

from MessageCommon import *

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
                return self.__commandWorkExecutionAnnouncement(aData)

            elif aMessageName == 'DetermineGraphCycleRequest':
                return self.__determineGraphCycleRequest(aData)

            elif aMessageName == 'DetermineGraphCycleResponse':
                return self.__determineGraphCycleResponse(aData)

            elif aMessageName == 'DetermineWorkCycleRequest':
                return self.__determineWorkCycleRequest(aData)

            elif aMessageName == 'DetermineWorkCycleResponse':
                return self.__determineWorkCycleResponse(aData)

            elif aMessageName == 'ExecuteGraphAnnouncement':
                return self.__executeGraphAnnouncement(aData)

            elif aMessageName == 'ExecuteWorkAnnouncement':
                return self.__executeWorkAnnouncement(aData)

            elif aMessageName == 'HeartbeatAnnouncement':
                return self.__heartbeatAnnouncement(aData)

            elif aMessageName == 'LoadGraphAndWorkRequest':
                return self.__loadGraphAndWorkRequest(aData)

            elif aMessageName == 'LoadGraphAndWorkResponse':
                return self.__loadGraphAndWorkResponse(aData)

            elif aMessageName == 'PokeAnnouncement':
                return self.__pokeAnnouncement(aData)

            elif aMessageName == 'PresentYourselfRequest':
                return self.__presentYourselfRequest(aData)

            elif aMessageName == 'PresentYourselfResponse':
                return self.__presentYourselfResponse(aData)

            elif aMessageName == 'ReportFinishedWorkAnnouncement':
                return self.__reportFinishedWorkAnnouncement(aData)

            else:
                # TODO: Handle this more gracefully
                print "Invalid message."
                sys.exit(1)

        except KeyError, e:
            # TODO: Handle this more gracefully
            print e
            sys.exit(1)

    def __commandWorkExecutionAnnouncement(self, aData):
        """Encodes CommandWorkExecutionAnnouncement.

        Arguments:
            aData: The data.

        Returns:
            CommandWorkExecutionAnnouncement envelope.

        """
        payload = Messages_pb2.CommandWorkExecutionAnnouncement()
        payload.messageName = 'CommandWorkExecutionAnnouncement'
        payload.sender.type = aData['sender'].mType
        payload.sender.nick = aData['sender'].mNick
        payload.graphName   = aData['graphName']
        payload.cycle       = aData['cycle']
        payload.workName    = aData['workName']

        return self.__putIntoAnEnvelope(COMMAND_WORK_EXECUTION_ANNOUNCEMENT, payload)

    def __determineGraphCycleRequest(self, aData):
        """Encodes DetermineGraphCycleRequest.

        Arguments:
            aData: The data.

        Returns:
            DetermineGraphCycleRequest envelope.

        """
        payload = Messages_pb2.DetermineGraphCycleRequest()
        payload.messageName = 'DetermineGraphCycleRequest'
        payload.sender.type = aData['sender'].mType
        payload.sender.nick = aData['sender'].mNick
        payload.graphName   = aData['graphName']

        return self.__putIntoAnEnvelope(DETERMINE_GRAPH_CYCLE_REQUEST, payload)

    def __determineGraphCycleResponse(self, aData):
        """Encodes DetermineGraphCycleResponse.

        Arguments:
            aData: The data.

        Returns:
            DetermineGraphCycleResponse envelope.

        """
        payload = Messages_pb2.DetermineGraphCycleResponse()
        payload.messageName   = 'DetermineGraphCycleResponse'
        payload.sender.type   = aData['sender'].mType
        payload.sender.nick   = aData['sender'].mNick
        payload.receiver.type = aData['receiver'].mType
        payload.receiver.nick = aData['receiver'].mNick
        payload.graphName     = aData['graphName']
        payload.cycle         = aData['cycle']

        return self.__putIntoAnEnvelope(DETERMINE_GRAPH_CYCLE_RESPONSE, payload)

    def __determineWorkCycleRequest(self, aData):
        """Encodes DetermineWorkCycleRequest.

        Arguments:
            aData: The data.

        Returns:
            DetermineWorkCycleRequest envelope.

        """
        payload = Messages_pb2.DetermineWorkCycleRequest()
        payload.messageName = 'DetermineWorkCycleRequest'
        payload.sender.type = aData['sender'].mType
        payload.sender.nick = aData['sender'].mNick
        payload.graphName   = aData['graphName']
        payload.cycle       = aData['cycle']
        payload.workName    = aData['workName']

        return self.__putIntoAnEnvelope(DETERMINE_WORK_CYCLE_REQUEST, payload)

    def __determineWorkCycleResponse(self, aData):
        """Encodes DetermineWorkCycleResponse.

        Arguments:
            aData: The data.

        Returns:
            DetermineWorkCycleResponse envelope.

        """
        payload = Messages_pb2.DetermineWorkCycleResponse()
        payload.messageName   = 'DetermineWorkCycleResponse'
        payload.sender.type   = aData['sender'].mType
        payload.sender.nick   = aData['sender'].mNick
        payload.receiver.type = aData['receiver'].mType
        payload.receiver.nick = aData['receiver'].mNick
        payload.graphName     = aData['graphName']
        payload.cycle         = aData['cycle']
        payload.workName      = aData['workName']
        payload.workCycle     = aData['workCycle']

        return self.__putIntoAnEnvelope(DETERMINE_WORK_CYCLE_RESPONSE, payload)

    def __executeGraphAnnouncement(self, aData):
        """Encodes ExecuteGraphAnnouncement.

        Arguments:
            aData: The data.

        Returns:
            ExecuteGraphAnnouncement envelope.

        """
        payload = Messages_pb2.ExecuteGraphAnnouncement()
        payload.messageName = 'ExecuteGraphAnnouncement'
        payload.sender.type = aData['sender'].mType
        payload.sender.nick = aData['sender'].mNick
        payload.graphName   = aData['graphName']

        return self.__putIntoAnEnvelope(EXECUTE_GRAPH_ANNOUNCEMENT, payload)

    def __executeWorkAnnouncement(self, aData):
        """Encodes ExecuteWorkAnnouncement.

        Arguments:
            aData: The data.

        Returns:
            ExecuteWorkAnnouncement envelope.

        """
        payload = Messages_pb2.ExecuteWorkAnnouncement()
        payload.messageName   = 'ExecuteWorkAnnouncement'
        payload.sender.type   = aData['sender'].mType
        payload.sender.nick   = aData['sender'].mNick
        payload.receiver.type = aData['receiver'].mType
        payload.receiver.nick = aData['receiver'].mNick
        payload.graphName     = aData['graphName']
        payload.cycle         = aData['cycle']
        payload.workName      = aData['workName']

        return self.__putIntoAnEnvelope(EXECUTE_WORK_ANNOUNCEMENT, payload)

    def __heartbeatAnnouncement(self, aData):
        """Encodes HeartbeatAnnouncement.

        Arguments:
            aData: The data.

        Returns:
            HeartbeatAnnouncement envelope.

        """
        payload = Messages_pb2.HeartbeatAnnouncement()
        payload.messageName = 'HeartbeatAnnouncement'
        payload.sender.type = aData['sender'].mType
        payload.sender.nick = aData['sender'].mNick
        payload.timestamp   = aData['timestamp']

        return self.__putIntoAnEnvelope(HEARTBEAT_ANNOUNCEMENT, payload)

    def __loadGraphAndWorkRequest(self, aData):
        """Encodes LoadGraphAndWorkRequest.

        Arguments:
            aData: The data.

        Returns:
            LoadGraphAndWorkRequest envelope.

        """
        payload = Messages_pb2.LoadGraphAndWorkRequest()
        payload.messageName = 'LoadGraphAndWorkRequest'
        payload.sender.type = aData['sender'].mType
        payload.sender.nick = aData['sender'].mNick

        return self.__putIntoAnEnvelope(LOAD_GRAPH_AND_WORK_REQUEST, payload)

    def __loadGraphAndWorkResponse(self, aData):
        """Encodes LoadGraphAndWorkResponse.

        Arguments:
            aData: The data.

        Returns:
            LoadGraphAndWorkResponse envelope.

        """
        payload = Messages_pb2.LoadGraphAndWorkResponse()
        payload.messageName   = 'LoadGraphAndWorkResponse'
        payload.sender.type   = aData['sender'].mType
        payload.sender.nick   = aData['sender'].mNick
        payload.receiver.type = aData['receiver'].mType
        payload.receiver.nick = aData['receiver'].mNick

        for graphDictionary in aData['graphs']:
            graphData = Messages_pb2.GraphData()
            graphData.graphName = graphDictionary['graphName']
            payload.graphs.extend([graphData])

        for workDictionary in aData['works']:
            workData = Messages_pb2.WorkData()
            workData.graphName = workDictionary['graphName']
            workData.workName = workDictionary['workName']
            payload.works.extend([workData])

        for workPredecessorDictionary in aData['workPredecessors']:
            workPredecessorData = Messages_pb2.WorkPredecessorData()
            workPredecessorData.workName = workPredecessorDictionary['workName']
            workPredecessorData.predecessorWorkName = workPredecessorDictionary['predecessorWorkName']
            payload.workPredecessors.extend([workPredecessorData])

        return self.__putIntoAnEnvelope(LOAD_GRAPH_AND_WORK_RESPONSE, payload)

    def __pokeAnnouncement(self, aData):
        """Encodes PokeAnnouncement.

        Arguments:
            aData: The data.

        Returns:
            PokeAnnouncement envelope.

        """
        payload = Messages_pb2.PokeAnnouncement()
        payload.messageName = 'PokeAnnouncement'
        payload.sender.type = aData['sender'].mType
        payload.sender.nick = aData['sender'].mNick

        return self.__putIntoAnEnvelope(POKE_ANNOUNCEMENT, payload)

    def __presentYourselfRequest(self, aData):
        """Encodes PresentYourselfRequest.

        Arguments:
            aData: The data.

        Returns:
            PresentYourselfRequest envelope.

        """
        payload = Messages_pb2.PresentYourselfRequest()
        payload.messageName   = 'PresentYourselfRequest'
        payload.sender.type   = aData['sender'].mType
        payload.sender.nick   = aData['sender'].mNick
        payload.receiver.type = aData['receiver'].mType
        payload.receiver.nick = aData['receiver'].mNick

        return self.__putIntoAnEnvelope(PRESENT_YOURSELF_REQUEST, payload)

    def __presentYourselfResponse(self, aData):
        """Encodes PresentYourselfResponse.

        Arguments:
            aData: The data.

        Returns:
            PresentYourselfResponse envelope.

        """
        payload = Messages_pb2.PresentYourselfResponse()
        payload.messageName   = 'PresentYourselfResponse'
        payload.sender.type   = aData['sender'].mType
        payload.sender.nick   = aData['sender'].mNick
        payload.receiver.type = aData['receiver'].mType
        payload.receiver.nick = aData['receiver'].mNick

        return self.__putIntoAnEnvelope(PRESENT_YOURSELF_RESPONSE, payload)

    def __reportFinishedWorkAnnouncement(self, aData):
        """Encodes ReportFinishedWorkAnnouncement

        Arguments:
            aData: The data.

        Returns:
            ReportFinishedWorkAnnouncement envelope.

        """
        payload = Messages_pb2.ReportFinishedWorkAnnouncement()
        payload.messageName = 'ReportFinishedWorkAnnouncement'
        payload.sender.type = aData['sender'].mType
        payload.sender.nick = aData['sender'].mNick
        payload.graphName   = aData['graphName']
        payload.graphCycle  = aData['graphCycle']
        payload.workName    = aData['workName']
        payload.workCycle   = aData['workCycle']
        payload.result      = aData['result']

        return self.__putIntoAnEnvelope(REPORT_FINISHED_WORK_ANNOUNCEMENT, payload)

    def __putIntoAnEnvelope(self, aId, aPayload):
        """Puts the payload into an envelope.

        Arguments:
            aId:      The id of a header.
            aPayload: The payload.

        Returns:
            The envelope.

        """
        envelope = Messages_pb2.Envelope()
        envelope.header.id       = aId
        envelope.payload.payload = aPayload.SerializeToString()

        return envelope
