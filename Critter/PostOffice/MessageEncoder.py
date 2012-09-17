"""The message encoder."""

import sys

import Messages_pb2

from Messages_pb2  import *
from MessageCommon import *

class MessageEncoder(object):
    """The message encoder delivers a message encoded in protobuf based upon delivered parameters.

    For all messages the parameters are taken, and an envelope is returned.

    """

    def encode(self, aMessage):
        """Encodes a message based upon the dictionary.

        Arguments:
            aMessage: The data.

        Returns:
            A message.

        """
        classToBeInstantiated = getattr(Messages_pb2, aMessage['messageName'])
        message = classToBeInstantiated()
        self.__setMessageField(message, aMessage)
        return message

    def putIntoAnEnvelope(self, aMessage):
        """A method needed to have one interface for creating messages everywhere.

        Arguments:
            aMessage: The message.

        Returns:
            The message in an envelope.

        """
        try:
            if False: pass
            elif aMessage.messageName == 'Announcement_Heartbeat':          return self.__putIntoAnEnvelope(ANNOUNCEMENT_HEARTBEAT, aMessage)
            elif aMessage.messageName == 'Announcement_Poke':               return self.__putIntoAnEnvelope(ANNOUNCEMENT_POKE, aMessage)
            elif aMessage.messageName == 'Command_DescribeCrittwork_Req':   return self.__putIntoAnEnvelope(COMMAND_DESCRIBE_CRITTWORK_REQ, aMessage)
            elif aMessage.messageName == 'Command_DescribeCrittwork_Res':   return self.__putIntoAnEnvelope(COMMAND_DESCRIBE_CRITTWORK_RES, aMessage)
            elif aMessage.messageName == 'Command_DetermineGraphCycle_Req': return self.__putIntoAnEnvelope(COMMAND_DETERMINE_GRAPH_CYCLE_REQ, aMessage)
            elif aMessage.messageName == 'Command_DetermineGraphCycle_Res': return self.__putIntoAnEnvelope(COMMAND_DETERMINE_GRAPH_CYCLE_RES, aMessage)
            elif aMessage.messageName == 'Command_DetermineWorkCycle_Req':  return self.__putIntoAnEnvelope(COMMAND_DETERMINE_WORK_CYCLE_REQ, aMessage)
            elif aMessage.messageName == 'Command_DetermineWorkCycle_Res':  return self.__putIntoAnEnvelope(COMMAND_DETERMINE_WORK_CYCLE_RES, aMessage)
            elif aMessage.messageName == 'Command_Election_Req':            return self.__putIntoAnEnvelope(COMMAND_ELECTION_REQ, aMessage)
            elif aMessage.messageName == 'Command_Election_Res':            return self.__putIntoAnEnvelope(COMMAND_ELECTION_RES, aMessage)
            elif aMessage.messageName == 'Command_ExecuteGraph_Req':        return self.__putIntoAnEnvelope(COMMAND_EXECUTE_GRAPH_REQ, aMessage)
            elif aMessage.messageName == 'Command_ExecuteGraph_Res':        return self.__putIntoAnEnvelope(COMMAND_EXECUTE_GRAPH_RES, aMessage)
            elif aMessage.messageName == 'Command_ExecuteWork_Req':         return self.__putIntoAnEnvelope(COMMAND_EXECUTE_WORK_REQ, aMessage)
            elif aMessage.messageName == 'Command_ExecuteWork_Res':         return self.__putIntoAnEnvelope(COMMAND_EXECUTE_WORK_RES, aMessage)
            elif aMessage.messageName == 'Command_LoadGraphAndWork_Req':    return self.__putIntoAnEnvelope(COMMAND_LOAD_GRAPH_AND_WORK_REQ, aMessage)
            elif aMessage.messageName == 'Command_LoadGraphAndWork_Res':    return self.__putIntoAnEnvelope(COMMAND_LOAD_GRAPH_AND_WORK_RES, aMessage)
            elif aMessage.messageName == 'Command_LoadGraphDetails_Req':    return self.__putIntoAnEnvelope(COMMAND_LOAD_GRAPH_DETAILS_REQ, aMessage)
            elif aMessage.messageName == 'Command_LoadGraphDetails_Res':    return self.__putIntoAnEnvelope(COMMAND_LOAD_GRAPH_DETAILS_RES, aMessage)
            elif aMessage.messageName == 'Command_LoadWorkDetails_Req':     return self.__putIntoAnEnvelope(COMMAND_LOAD_WORK_DETAILS_REQ, aMessage)
            elif aMessage.messageName == 'Command_LoadWorkDetails_Res':     return self.__putIntoAnEnvelope(COMMAND_LOAD_WORK_DETAILS_RES, aMessage)
            elif aMessage.messageName == 'Command_OrderWorkExecution_Req':  return self.__putIntoAnEnvelope(COMMAND_ORDER_WORK_EXECUTION_REQ, aMessage)
            elif aMessage.messageName == 'Command_OrderWorkExecution_Res':  return self.__putIntoAnEnvelope(COMMAND_ORDER_WORK_EXECUTION_RES, aMessage)
            elif aMessage.messageName == 'Command_PresentYourself_Req':     return self.__putIntoAnEnvelope(COMMAND_PRESENT_YOURSELF_REQ, aMessage)
            elif aMessage.messageName == 'Command_PresentYourself_Res':     return self.__putIntoAnEnvelope(COMMAND_PRESENT_YOURSELF_RES, aMessage)
            else:
                # TODO: Handle this more gracefully
                print "Invalid message."
                sys.exit(1)

        except KeyError, e:
            # TODO: Handle this more gracefully
            print e
            sys.exit(1)

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
