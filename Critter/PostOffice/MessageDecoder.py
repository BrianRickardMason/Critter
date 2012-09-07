"""The message decoder."""

import Messages_pb2

from MessageCommon import *

class MessageDecoder(object):
    """The message decoder delivers the content of received bytes in a form of a class.

    For all messages the received bytes are taken, and classes are returned.

    """

    def decode(self, aBytesRead):
        """Decodes the bytes into the form of a message.

        Returns a class representing the message, None if decode error happened.

        """
        envelope = Messages_pb2.Envelope()
        envelope.ParseFromString(aBytesRead)

        # TODO: Clean me up fast!

        if False: pass
        elif envelope.header.id == CANT_EXECUTE_WORK_NOW_ANNOUNCEMENT: message = Messages_pb2.CantExecuteWorkNowAnnouncement()
        elif envelope.header.id == COMMAND_DETERMINE_GRAPH_CYCLE_REQ:  message = Messages_pb2.Command_DetermineGraphCycle_Req()
        elif envelope.header.id == COMMAND_DETERMINE_GRAPH_CYCLE_RES:  message = Messages_pb2.Command_DetermineGraphCycle_Res()
        elif envelope.header.id == COMMAND_DETERMINE_WORK_CYCLE_REQ:   message = Messages_pb2.Command_DetermineWorkCycle_Req()
        elif envelope.header.id == COMMAND_DETERMINE_WORK_CYCLE_RES:   message = Messages_pb2.Command_DetermineWorkCycle_Res()
        elif envelope.header.id == COMMAND_ELECTION_REQ:               message = Messages_pb2.Command_Election_Req()
        elif envelope.header.id == COMMAND_ELECTION_RES:               message = Messages_pb2.Command_Election_Res()
        elif envelope.header.id == COMMAND_EXECUTE_GRAPH_REQ:          message = Messages_pb2.Command_ExecuteGraph_Req()
        elif envelope.header.id == COMMAND_EXECUTE_GRAPH_RES:          message = Messages_pb2.Command_ExecuteGraph_Res()
        elif envelope.header.id == COMMAND_EXECUTE_WORK_REQ:           message = Messages_pb2.Command_ExecuteWork_Req()
        elif envelope.header.id == COMMAND_EXECUTE_WORK_RES:           message = Messages_pb2.Command_ExecuteWork_Res()
        elif envelope.header.id == COMMAND_LOAD_GRAPH_AND_WORK_REQ:    message = Messages_pb2.Command_LoadGraphAndWork_Req()
        elif envelope.header.id == COMMAND_LOAD_GRAPH_AND_WORK_RES:    message = Messages_pb2.Command_LoadGraphAndWork_Res()
        elif envelope.header.id == COMMAND_LOAD_GRAPH_DETAILS_REQ:     message = Messages_pb2.Command_LoadGraphDetails_Req()
        elif envelope.header.id == COMMAND_LOAD_GRAPH_DETAILS_RES:     message = Messages_pb2.Command_LoadGraphDetails_Res()
        elif envelope.header.id == COMMAND_LOAD_WORK_DETAILS_REQ:      message = Messages_pb2.Command_LoadWorkDetails_Req()
        elif envelope.header.id == COMMAND_LOAD_WORK_DETAILS_RES:      message = Messages_pb2.Command_LoadWorkDetails_Res()
        elif envelope.header.id == COMMAND_ORDER_WORK_EXECUTION_REQ:   message = Messages_pb2.Command_OrderWorkExecution_Req()
        elif envelope.header.id == COMMAND_ORDER_WORK_EXECUTION_RES:   message = Messages_pb2.Command_OrderWorkExecution_Res()
        elif envelope.header.id == HEARTBEAT_ANNOUNCEMENT:             message = Messages_pb2.HeartbeatAnnouncement()
        elif envelope.header.id == POKE_ANNOUNCEMENT:                  message = Messages_pb2.PokeAnnouncement()
        elif envelope.header.id == PRESENT_YOURSELF_REQUEST:           message = Messages_pb2.PresentYourselfRequest()
        elif envelope.header.id == PRESENT_YOURSELF_RESPONSE:          message = Messages_pb2.PresentYourselfResponse()
        else:                                                          return None

        message.ParseFromString(envelope.payload.payload)
        return message
