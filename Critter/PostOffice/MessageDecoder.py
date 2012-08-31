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

        if   envelope.header.id == CANT_EXECUTE_WORK_NOW_ANNOUNCEMENT:      message = Messages_pb2.CantExecuteWorkNowAnnouncement()
        elif envelope.header.id == COMMAND_WORK_EXECUTION_ANNOUNCEMENT:     message = Messages_pb2.CommandWorkExecutionAnnouncement()
        elif envelope.header.id == DETERMINE_GRAPH_CYCLE_REQUEST:           message = Messages_pb2.DetermineGraphCycleRequest()
        elif envelope.header.id == DETERMINE_GRAPH_CYCLE_RESPONSE:          message = Messages_pb2.DetermineGraphCycleResponse()
        elif envelope.header.id == DETERMINE_WORK_CYCLE_REQUEST:            message = Messages_pb2.DetermineWorkCycleRequest()
        elif envelope.header.id == DETERMINE_WORK_CYCLE_RESPONSE:           message = Messages_pb2.DetermineWorkCycleResponse()
        elif envelope.header.id == EXECUTE_GRAPH_ANNOUNCEMENT:              message = Messages_pb2.ExecuteGraphAnnouncement()
        elif envelope.header.id == EXECUTE_WORK_ANNOUNCEMENT:               message = Messages_pb2.ExecuteWorkAnnouncement()
        elif envelope.header.id == HEARTBEAT_ANNOUNCEMENT:                  message = Messages_pb2.HeartbeatAnnouncement()
        elif envelope.header.id == LOAD_GRAPH_AND_WORK_REQUEST:             message = Messages_pb2.LoadGraphAndWorkRequest()
        elif envelope.header.id == LOAD_GRAPH_AND_WORK_RESPONSE:            message = Messages_pb2.LoadGraphAndWorkResponse()
        elif envelope.header.id == LOAD_WORK_DETAILS_REQUEST:               message = Messages_pb2.LoadWorkDetailsRequest()
        elif envelope.header.id == LOAD_WORK_DETAILS_RESPONSE:              message = Messages_pb2.LoadWorkDetailsResponse()
        elif envelope.header.id == POKE_ANNOUNCEMENT:                       message = Messages_pb2.PokeAnnouncement()
        elif envelope.header.id == PRESENT_YOURSELF_REQUEST:                message = Messages_pb2.PresentYourselfRequest()
        elif envelope.header.id == PRESENT_YOURSELF_RESPONSE:               message = Messages_pb2.PresentYourselfResponse()
        elif envelope.header.id == REPORT_FINISHED_WORK_ANNOUNCEMENT:       message = Messages_pb2.ReportFinishedWorkAnnouncement()
        elif envelope.header.id == EXECUTE_GRAPH_SEEK_VOLUNTEERS:           message = Messages_pb2.ExecuteGraphSeekVolunteers()
        elif envelope.header.id == EXECUTE_GRAPH_VOLUNTEE:                  message = Messages_pb2.ExecuteGraphVoluntee()
        elif envelope.header.id == EXECUTE_GRAPH_SELECT_VOLUNTEER:          message = Messages_pb2.ExecuteGraphSelectVolunteer()
        elif envelope.header.id == COMMAND_WORK_EXECUTION_SEEK_VOLUNTEERS:  message = Messages_pb2.CommandWorkExecutionSeekVolunteers()
        elif envelope.header.id == COMMAND_WORK_EXECUTION_VOLUNTEE:         message = Messages_pb2.CommandWorkExecutionVoluntee()
        elif envelope.header.id == COMMAND_WORK_EXECUTION_SELECT_VOLUNTEER: message = Messages_pb2.CommandWorkExecutionSelectVolunteer()
        elif envelope.header.id == COMMAND_REQ_EXECUTE_GRAPH:               message = Messages_pb2.Command_Req_ExecuteGraph()
        elif envelope.header.id == COMMAND_RES_EXECUTE_GRAPH:               message = Messages_pb2.Command_Res_ExecuteGraph()
        elif envelope.header.id == COMMAND_REQ_ELECTION:                    message = Messages_pb2.Command_Req_Election()
        elif envelope.header.id == COMMAND_RES_ELECTION:                    message = Messages_pb2.Command_Res_Election()
        elif envelope.header.id == COMMAND_REQ_DETERMINE_GRAPH_CYCLE:       message = Messages_pb2.Command_Req_DetermineGraphCycle()
        elif envelope.header.id == COMMAND_RES_DETERMINE_GRAPH_CYCLE:       message = Messages_pb2.Command_Res_DetermineGraphCycle()
        elif envelope.header.id == COMMAND_REQ_ORDER_WORK_EXECUTION:        message = Messages_pb2.Command_Req_OrderWorkExecution()
        elif envelope.header.id == COMMAND_RES_ORDER_WORK_EXECUTION:        message = Messages_pb2.Command_Res_OrderWorkExecution()
        else:                                                               return None

        message.ParseFromString(envelope.payload.payload)
        return message
