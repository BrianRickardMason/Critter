"""The message decoder."""

import Messages_pb2

from MessageCommon import *

class MessageDecoder(object):
    """The message decoder delivers the content of received bytes in a form of a class.

    For all messages the received bytes are taken, and classes are returned.

    """

    def decode(self, aSerializedEnvelope):
        """Decodes the serialized envelope into the form of a message.

        Returns a message, None if decode error happened.

        """
        envelope = Messages_pb2.Envelope()
        # TODO: Protect if from the garbage.
        envelope.ParseFromString(aSerializedEnvelope)

        # TODO: Clean me up fast!

        if False: pass
        elif envelope.header.id == ANNOUNCEMENT_HEARTBEAT:            message = Messages_pb2.Announcement_Heartbeat()
        elif envelope.header.id == ANNOUNCEMENT_POKE:                 message = Messages_pb2.Announcement_Poke()
        elif envelope.header.id == COMMAND_DESCRIBE_CRITTWORK_REQ:    message = Messages_pb2.Command_DescribeCrittwork_Req()
        elif envelope.header.id == COMMAND_DESCRIBE_CRITTWORK_RES:    message = Messages_pb2.Command_DescribeCrittwork_Res()
        elif envelope.header.id == COMMAND_DETERMINE_GRAPH_CYCLE_REQ: message = Messages_pb2.Command_DetermineGraphCycle_Req()
        elif envelope.header.id == COMMAND_DETERMINE_GRAPH_CYCLE_RES: message = Messages_pb2.Command_DetermineGraphCycle_Res()
        elif envelope.header.id == COMMAND_DETERMINE_WORK_CYCLE_REQ:  message = Messages_pb2.Command_DetermineWorkCycle_Req()
        elif envelope.header.id == COMMAND_DETERMINE_WORK_CYCLE_RES:  message = Messages_pb2.Command_DetermineWorkCycle_Res()
        elif envelope.header.id == COMMAND_ELECTION_REQ:              message = Messages_pb2.Command_Election_Req()
        elif envelope.header.id == COMMAND_ELECTION_RES:              message = Messages_pb2.Command_Election_Res()
        elif envelope.header.id == COMMAND_EXECUTE_GRAPH_REQ:         message = Messages_pb2.Command_ExecuteGraph_Req()
        elif envelope.header.id == COMMAND_EXECUTE_GRAPH_RES:         message = Messages_pb2.Command_ExecuteGraph_Res()
        elif envelope.header.id == COMMAND_EXECUTE_WORK_REQ:          message = Messages_pb2.Command_ExecuteWork_Req()
        elif envelope.header.id == COMMAND_EXECUTE_WORK_RES:          message = Messages_pb2.Command_ExecuteWork_Res()
        elif envelope.header.id == COMMAND_LOAD_GRAPH_AND_WORK_REQ:   message = Messages_pb2.Command_LoadGraphAndWork_Req()
        elif envelope.header.id == COMMAND_LOAD_GRAPH_AND_WORK_RES:   message = Messages_pb2.Command_LoadGraphAndWork_Res()
        elif envelope.header.id == COMMAND_LOAD_GRAPH_DETAILS_REQ:    message = Messages_pb2.Command_LoadGraphDetails_Req()
        elif envelope.header.id == COMMAND_LOAD_GRAPH_DETAILS_RES:    message = Messages_pb2.Command_LoadGraphDetails_Res()
        elif envelope.header.id == COMMAND_LOAD_WORK_DETAILS_REQ:     message = Messages_pb2.Command_LoadWorkDetails_Req()
        elif envelope.header.id == COMMAND_LOAD_WORK_DETAILS_RES:     message = Messages_pb2.Command_LoadWorkDetails_Res()
        elif envelope.header.id == COMMAND_ORDER_WORK_EXECUTION_REQ:  message = Messages_pb2.Command_OrderWorkExecution_Req()
        elif envelope.header.id == COMMAND_ORDER_WORK_EXECUTION_RES:  message = Messages_pb2.Command_OrderWorkExecution_Res()
        elif envelope.header.id == COMMAND_PRESENT_YOURSELF_REQ:      message = Messages_pb2.Command_PresentYourself_Req()
        elif envelope.header.id == COMMAND_PRESENT_YOURSELF_RES:      message = Messages_pb2.Command_PresentYourself_Res()
        else:                                                         return None

        message.ParseFromString(envelope.payload.payload)
        return message
