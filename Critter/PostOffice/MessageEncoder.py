"""The message encoder."""

import sys

import Messages_pb2

from Messages_pb2  import *
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
            if False: pass
            elif aMessageName == 'CantExecuteWorkNowAnnouncement':      return self.__encode(CANT_EXECUTE_WORK_NOW_ANNOUNCEMENT, aData)
            elif aMessageName == 'HeartbeatAnnouncement':               return self.__encode(HEARTBEAT_ANNOUNCEMENT, aData)
            elif aMessageName == 'LoadGraphAndWorkRequest':             return self.__encode(LOAD_GRAPH_AND_WORK_REQUEST, aData)
            elif aMessageName == 'LoadGraphAndWorkResponse':            return self.__encode(LOAD_GRAPH_AND_WORK_RESPONSE, aData)
            elif aMessageName == 'LoadWorkDetailsRequest':              return self.__encode(LOAD_WORK_DETAILS_REQUEST, aData)
            elif aMessageName == 'LoadWorkDetailsResponse':             return self.__encode(LOAD_WORK_DETAILS_RESPONSE, aData)
            elif aMessageName == 'PokeAnnouncement':                    return self.__encode(POKE_ANNOUNCEMENT, aData)
            elif aMessageName == 'PresentYourselfRequest':              return self.__encode(PRESENT_YOURSELF_REQUEST, aData)
            elif aMessageName == 'PresentYourselfResponse':             return self.__encode(PRESENT_YOURSELF_RESPONSE, aData)
            elif aMessageName == 'Command_Req_ExecuteGraph':            return self.__encode(COMMAND_EXECUTE_GRAPH_REQ, aData)
            elif aMessageName == 'Command_Res_ExecuteGraph':            return self.__encode(COMMAND_EXECUTE_GRAPH_RES, aData)
            elif aMessageName == 'Command_Req_Election':                return self.__encode(COMMAND_ELECTION_REQ, aData)
            elif aMessageName == 'Command_Res_Election':                return self.__encode(COMMAND_ELECTION_RES, aData)
            elif aMessageName == 'Command_Req_DetermineGraphCycle':     return self.__encode(COMMAND_DETERMINE_GRAPH_CYCLE_REQ, aData)
            elif aMessageName == 'Command_Res_DetermineGraphCycle':     return self.__encode(COMMAND_DETERMINE_GRAPH_CYCLE_RES, aData)
            elif aMessageName == 'Command_Req_OrderWorkExecution':      return self.__encode(COMMAND_ORDER_WORK_EXECUTION_REQ, aData)
            elif aMessageName == 'Command_Res_OrderWorkExecution':      return self.__encode(COMMAND_ORDER_WORK_EXECUTION_RES, aData)
            elif aMessageName == 'Command_Req_ExecuteWork':             return self.__encode(COMMAND_EXECUTE_WORK_REQ, aData)
            elif aMessageName == 'Command_Res_ExecuteWork':             return self.__encode(COMMAND_EXECUTE_WORK_RES, aData)
            elif aMessageName == 'Command_Req_DetermineWorkCycle':      return self.__encode(COMMAND_DETERMINE_WORK_CYCLE_REQ, aData)
            elif aMessageName == 'Command_Res_DetermineWorkCycle':      return self.__encode(COMMAND_DETERMINE_WORK_CYCLE_RES, aData)
            else:
                # TODO: Handle this more gracefully
                print "Invalid message."
                sys.exit(1)

        except KeyError, e:
            # TODO: Handle this more gracefully
            print e
            sys.exit(1)

    def __encode(self, aHeaderId, aData):
        """Encodes a message based upon the dictionary.

        Arguments:
            aData: The data.

        Returns:
            An envelope.

        """
        classToBeInstantiated = getattr(Messages_pb2, aData['messageName'])
        payload = classToBeInstantiated()
        self.__setMessageField(payload, aData)
        return self.__putIntoAnEnvelope(aHeaderId, payload)

    def __setMessageField(self, aPayload, aDictionary):
        """Recursively sets a message field.

        Arguments:
            aPayload:    The payload holding the message.
            aDictionary: The dictionary describing the message.

        """
        for key in aDictionary.iterkeys():
            if type(aDictionary[key]) is dict:
                payload    = getattr(aPayload, key)
                dictionary = aDictionary[key]
                self.__setMessageField(payload, dictionary)
            elif type(aDictionary[key]) is list:
                payload    = getattr(aPayload, key)
                dictionary = aDictionary[key]
                for item in dictionary:
                    tmpPayload = payload.add()
                    self.__setMessageField(tmpPayload, item)
            else:
                setattr(aPayload, key, aDictionary[key])

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
