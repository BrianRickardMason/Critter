"""The message encoder."""

import sys

import Messages_pb2

from Messages_pb2  import *
from MessageCommon import *

class MessageEncoder(object):
    """The message encoder delivers a message encoded in protobuf based upon delivered parameters.

    For all messages the parameters are taken, and an envelope is returned.

    """

    def encode(self, aMessageDictionary):
        classToBeInstantiated = getattr(Messages_pb2, aMessageDictionary['messageName'])
        message = classToBeInstantiated()
        self.__setMessageField(message, aMessageDictionary)
        return message

    def putIntoAnEnvelope(self, aMessage):
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

    def __setMessageField(self, aPayload, aMessageDictionary):
        for key in aMessageDictionary.iterkeys():
            if type(aMessageDictionary[key]) is dict:
                payload    = getattr(aPayload, key)
                dictionary = aMessageDictionary[key]
                self.__setMessageField(payload, dictionary)
            elif type(aMessageDictionary[key]) is list:
                payload    = getattr(aPayload, key)
                dictionary = aMessageDictionary[key]
                for item in dictionary:
                    tmpPayload = payload.add()
                    self.__setMessageField(tmpPayload, item)
            else:
                setattr(aPayload, key, aMessageDictionary[key])

    def __putIntoAnEnvelope(self, aId, aMessage):
        envelope = Messages_pb2.Envelope()
        envelope.header.id       = aId
        envelope.payload.payload = aMessage.SerializeToString()
        return envelope
