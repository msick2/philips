from ctypes import BigEndianStructure, Structure, c_int8, c_int16, c_int32, c_uint8, c_uint16, c_uint32, c_float



# = Typedef ============================================================================================================

#class RelativeTime(BigEndianStructure):
#    _pack_ = 1
#    _fields_ = [
#        ("RelativeTime", c_uint32),
#    ]
#
#
#class OIDType(BigEndianStructure):
#    _pack_ = 1
#    _fields_ = [
#        ("OIDType", c_uint16),
#    ]
#
#
#class MdsContext(BigEndianStructure):
#    _pack_ = 1
#    _fields_ = [
#        ("MdsContext", c_uint16),
#    ]
#
#
#class Handle(BigEndianStructure):
#    _pack_ = 1
#    _fields_ = [
#        ("Handle", c_uint16),
#    ]
#
#
#class ModifyOperator(BigEndianStructure):
#    _pack_ = 1
#    _fields_ = [
#        ("ModifyOperator", c_uint16),
#    ]


class I16(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("data", c_int16),
    ]

class U16(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("data", c_uint16),
    ]

class U32(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("data", c_uint32),
    ]

class FLOAT(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("data", c_float),
    ]

# = Basic Class ========================================================================================================

class FrameHdr(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("protocol_id", c_uint8),
        ("msg_type", c_uint8),
        ("length", c_uint16),
    ]

class RelativeTime(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("RelativeTime", c_uint32),
    ]

class AbsoluteTime(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("century", c_uint8),
        ("year", c_uint8),
        ("month", c_uint8),
        ("day", c_uint8),
        ("hour", c_uint8),
        ("minute", c_uint8),
        ("second", c_uint8),
        ("sec_fractions", c_uint8),
    ]


class SPpdu(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("session_id", c_uint16),  # contains a fixed value 0xE100
        ("p_context_id", c_uint16),  # negotiated in association phase, 2로 고정인듯?..
    ]


class ROapdus(BigEndianStructure):
    # define ROIV_APDU 1
    # define RORS_APDU 2
    # define ROER_APDU 3
    # define ROLRS_APDU 5
    _pack_ = 1
    _fields_ = [
        ("ro_type", c_uint16),  # ID for operation
        ("length", c_uint16),  # bytes to follow
    ]


class ROIVapdu(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("invoke_id", c_uint16),  # identifies the transaction
        ("command_type", c_uint16),  # identifies type of command
        ("length", c_uint16),  # no. of bytes in rest of message
    ]


class RORSapdu(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("invoke_id", c_uint16),  # mirrored back from op. invoke
        ("command_type", c_uint16),  # identifies type of command
        ("length", c_uint16),  # no. of bytes in rest of message
    ]

class ROLRSapdu(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("state", c_uint8),
        ("count", c_uint8),  # mirrored back from op. invoke
        ("invoke_id", c_uint16),  # mirrored back from op. invoke
        ("command_type", c_uint16),  # identifies type of command
        ("length", c_uint16),  # no. of bytes in rest of message
    ]


class ROERapdu(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("state", c_uint8),
        ("count", c_uint8),
        ("error_value", c_uint16),
        ("length", c_uint16),
    ]

#class RorlsId(BigEndianStructure):
#    # define RORLS_FIRST 1 /* set in the first message */
#    # define RORLS_NOT_FIRST_NOT_LAST 2
#    # define RORLS_LAST 3 /* last RORLSapdu, one RORSapdu
#    _pack_ = 1
#    _fields_ = [
#        ("state", c_uint8),
#        ("count", c_uint8),  # counter starts with 1
#    ]




#class GlbHandle(BigEndianStructure):
#    _pack_ = 1
#    _fields_ = [
#        ("context_id", c_uint16),
#        ("handle", c_uint16),
#    ]


#class ManagedObjectId(BigEndianStructure):
#    _pack_ = 1
#    _fields_ = [
#        ("m_obj_class", c_uint16),
#        ("context_id", c_uint16),
#        ("handle", c_uint16),
#    ]


class EventReportResult(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_obj_class", c_uint16),
        ("context_id", c_uint16),
        ("handle", c_uint16),  # mirrored from EvRep
        ("current_time", c_uint32),  # result time stamp
        ("event_type", c_uint16),  # identification of event
        ("length", c_uint16),  # size of appended data
    ]


class EventReportArgument(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_obj_class", c_uint16),
        ("context_id", c_uint16),
        ("handle", c_uint16),  # ident. of sender
        ("event_time", c_uint32),  # event time stamp
        ("event_type", c_uint16),  # identification of event
        ("length", c_uint16),  # size of appended data
    ]




class AVAType(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("attribute_id", c_uint16),
        ("length", c_uint16),
        #("attribute_val", c_uint16),
    ]


#class AVAType(BigEndianStructure):
#    _pack_ = 1
#    _fields_ = [
#        ("attribute_id", OIDType),
#        ("length", c_uint16),
#        ("attribute_val", c_uint16),
#    ]



class AttributeList(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("count", c_uint16),
        ("length", c_uint16),
        # ("value", list(AVAType)),
    ]


class ConnectIndInfo(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("count", c_uint16),
        ("length", c_uint16),
        # ("value", list(AVAType)),
    ]


class MdsCreateInfo(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_obj_class", c_uint16),
        ("context_id", c_uint16),
        ("handle", c_uint16),
        ("count", c_uint16),
        ("length", c_uint16),
        # ("value", list(AVAType)),
    ]


# = Variable Class =====================================================================================================


# ======================================================================================================================


class Header_Common(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("FrameHdr", FrameHdr),
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),
    ]


# class MDSCreateEventResult(BigEndianStructure):
#    _pack_ = 1
#    _fields_ = [
#        ("FrameHdr", FrameHdr),
#        ("SPpdu", SPpdu),
#        ("ROapdus", ROapdus),
#        ("EventReportResult", EventReportResult),
#    ]


class ConnectIndication(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("Nomenclature", c_uint32),
        ("ROapdus", ROapdus),                           # ro_type := ROIVapdu
        ("ROIVapdu", ROIVapdu),                         # command_type := CMD_EVENT_REPORT
        ("EventReportArgument", EventReportArgument),   # managed_object:={NOM_MOC_MDS_COMPOS_SINGLE_BED,0,0
                                                        # event_type := NOM_NOTI_MDS_CONNECT_INDIC
        ("ConnectIndInfo", ConnectIndInfo),
    ]


class MDSCreateEventReport(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),  # ro_type := ROIV_APDU
        ("ROIVapdu", ROIVapdu),  # command_type := CMD_CONFIRMED_EVENT_REPORT
        ("EventReportArgument", EventReportArgument),  # managed_object:={NOM_MOC_VMS_MDS,0,0
        # event_type := NOM_NOTI_MDS_CREAT
        ("MDSCreateInfo", MdsCreateInfo),
    ]


class MDSCreateEventResult(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),  # ro_type := RORS_APDU
        ("RORSapdu", RORSapdu),  # invoke_id := mirrored from event report
        # command_type := CMD_CONFIRMED_EVENT_REPORT
        ("EventReportResult", EventReportResult),  # managed_object := mirrored from event report
        # event_type := NOM_NOTI_MDS_CREAT
        # length := 0
    ]


# define NOM_ACT_POLL_MDIB_DATA 3094
# define NOM_ACT_POLL_MDIB_DATA_EXT 61755

class ActionArgument(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_obj_class", c_uint16),
        ("context_id", c_uint16),
        ("handle", c_uint16),  # addressed object
        ("scope", c_uint32),  # fixed value 0
        ("action_type", c_uint16),  # identification of method

        ("length", c_uint16),  # size of appended data
    ]


# define NOM_PART_OBJ 1
# define NOM_PART_SCADA 2
# define NOM_PART_EVT 3
# define NOM_PART_DIM 4
# define NOM_PART_PGRP 6
# define NOM_PART_INFRASTRUCT 8

#class NomPartition(BigEndianStructure):
#    _pack_ = 1
#    _fields_ = [
#        ("NomPartition", c_uint16),
#    ]


class TYPE(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("partition", c_uint16),
        ("code", c_uint16),
    ]


class PollMdibDataReq(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("poll_number", c_uint16),
        ("partition", c_uint16),
        ("code", c_uint16),
        ("polled_attr_grp", c_uint16),
    ]


class MDSPollAction(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),  # ro_type := ROIV_APDU
        ("ROIVapdu", ROIVapdu),  # command_type := CMD_CONFIRMED_ACTION
        ("ActionArgument", ActionArgument),  # managed_object := {NOM_MOC_VMS_MDS, 0, 0}
        # action_type := NOM_ACT_POLL_MDIB_DATA
        #("PollMdibDataReq", PollMdibDataReq),

    ]


class ActionResult(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_obj_class", c_uint16),
        ("context_id", c_uint16),
        ("handle", c_uint16),
        ("action_type", c_uint16),  # identification of method
        ("length", c_uint16),  # size of appended data
    ]


class ObservationPoll(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("obj_handle", c_uint16),
        ("count", c_uint16),
        ("length", c_uint16),
        #("value", list(AVAType)),  # identification of method
    ]


#class ObservationPoll(BigEndianStructure):
#    _pack_ = 1
#    _fields_ = [
#        ("obj_handle", Handle),
#        ("attributes", AttributeList),  # identification of method
#    ]


class poll_info(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("count", c_uint16),
        ("length", c_uint16),
        # ("value", list(ObservationPoll)),
    ]


class SingleContextPoll(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("context_id", c_uint16),
        ("count", c_uint16),
        ("length", c_uint16),
        # ("value", list(ObservationPoll)),
    ]

#class SingleContextPoll(BigEndianStructure):
#    _pack_ = 1
#    _fields_ = [
#        ("context_id", MdsContext),
#        ("poll_info", poll_info),
#    ]


class PollInfoList(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("count", c_uint16),
        ("length", c_uint16),
        # ("value", list(SingleContextPoll)),
    ]

class PollMdibDataReply(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("poll_number", c_uint16),
        ("rel_time_stamp", c_uint32),

        #("abs_time_stamp", AbsoluteTime),
        ("century", c_uint8),
        ("year", c_uint8),
        ("month", c_uint8),
        ("day", c_uint8),
        ("hour", c_uint8),
        ("minute", c_uint8),
        ("second", c_uint8),
        ("sec_fractions", c_uint8),

        ("partition", c_uint16),
        ("code", c_uint16),
        ("polled_attr_grp", c_uint16),
        #("poll_info_list", PollInfoList),
    ]

#class PollMdibDataReply(BigEndianStructure):
#    _pack_ = 1
#    _fields_ = [
#        ("poll_number", c_uint16),
#        ("rel_time_stamp", c_uint32),
#        ("abs_time_stamp", AbsoluteTime),
#        ("partition", c_uint16),
#        ("code", c_uint16),
#        ("polled_attr_grp", c_uint16),
#        ("poll_info_list", PollInfoList),
#    ]




class MDSPollActionResult(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),  # ro_type := RORS_APDU
        ("RORSapdu", RORSapdu),  # invoke_id := "mirrored from request message"
        # command_type := CMD_CONFIRMED_ACTION

        ("ActionResult", ActionResult),  # managed_object := {NOM_MOC_VMS_MDS, 0, 0}
        # action_type := NOM_ACT_POLL_MDIB_DATA
        # ("PollMdibDataReply", PollMdibDataReply),
    ]


class PollMdibDataReqExt(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("poll_number", c_uint16),
        ("partition", c_uint16),
        ("code", c_uint16),
        ("polled_attr_grp", c_uint16),
        ("poll_ext_attr", AttributeList),
    ]


#class MDSPollAction(BigEndianStructure):
#    _pack_ = 1
#    _fields_ = [
#        ("SPpdu", SPpdu),
#        ("ROapdus", ROapdus),  # ro_type := RORS_APDU
#        ("ROIVapdu", ROIVapdu),  # command_type := CMD_CONFIRMED_ACTION
#        ("ActionArgument", ActionArgument),  # managed_object := {NOM_MOC_VMS_MDS, 0, 0}
#        # action_type := NOM_ACT_POLL_MDIB_DATA_EXT
#        ("PollMdibDataReqExt", PollMdibDataReqExt),
#
#    ]


class PollMdibDataReplyExt(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("poll_number", c_uint16),
        ("sequence_no", c_uint16),

        ("rel_time_stamp", c_uint32),

        ("century", c_uint8),
        ("year", c_uint8),
        ("month", c_uint8),
        ("day", c_uint8),
        ("hour", c_uint8),
        ("minute", c_uint8),
        ("second", c_uint8),
        ("sec_fractions", c_uint8),

        ("partition", c_uint16),
        ("code", c_uint16),

        ("polled_attr_grp", c_uint16),
        # PollInfoList poll_info_list;

        #("count", c_uint16),
        #("length", c_uint16),
        # ("value", list(SingleContextPoll)),

        # u_16 poll_number;
        # u_16 sequence_no;
        # RelativeTime rel_time_stamp;
        # AbsoluteTime abs_time_stamp;
        # TYPE polled_obj_type;
        # OIDType polled_attr_grp;

    ]


class MDSPollActionResultExt(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),  # ro_type := RORS_APDU
        ("RORSapdu", RORSapdu),  # invoke_id := "mirrored from request message"
        # command_type := CMD_CONFIRMED_ACTION
        ("ActionResult", ActionResult),  # managed_object := {NOM_MOC_VMS_MDS, 0, 0}
        # action_type := NOM_ACT_POLL_MDIB_DATA_EXT
        # ("PollMdibDataReplyExt", PollMdibDataReplyExt),

    ]


class AttributeIdList(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("count", c_uint16),
        ("length", c_uint16),
        ("attributeIdList", c_uint16),
        # ("attributeIdList", list(OIDType)),
    ]


class GetArgument(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_obj_class", c_uint16),
        ("context_id", c_uint16),
        ("handle", c_uint16),
        ("scope", c_uint32),
        ("attributeIdList", AttributeIdList),
    ]


class MDSGetPriorityList(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),  # ro_type := ROIV_APDU
        ("ROIVapdu", ROIVapdu),  # command_type := CMD_GET
        ("GetArgument", GetArgument),  # managed_object := {NOM_MOC_VMS_MDS, 0, 0}
    ]


class GetResult(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_obj_class", c_uint16),
        ("context_id", c_uint16),
        ("handle", c_uint16),
        ("attributeList", AttributeList),
    ]


class MDSGetPriorityListResult(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),  # ro_type := RORS_APDU
        ("RORSapdu", RORSapdu),  # invoke_id := “mirrored from request message”,
        # command_type := CMD_GET
        ("GetResult", GetResult),  # managed_object := {NOM_MOC_VMS_MDS, 0, 0}
    ]


class AttributeModEntry(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("modifyOperator", c_uint16),
        ("attribute", AVAType),
    ]


class ModificationList(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("count", c_uint16),
        ("length", c_uint16),
        # ("value", list(AttributeModEntry)),
    ]


class SetArgument(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_obj_class", c_uint16),
        ("context_id", c_uint16),
        ("handle", c_uint16),
        ("ROapdus", c_uint32),
        ("modificationList", ModificationList),
    ]


class MDSSetPriorityList(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),  # ro_type := RORS_APDU
        ("ROIVapdu", ROIVapdu),  # invoke_id := “mirrored from request message”,
        # command_type := CMD_GET
        ("SetArgument", SetArgument),  # managed_object := {NOM_MOC_VMS_MDS, 0, 0}
    ]



class SetResult(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_obj_class", c_uint16),
        ("context_id", c_uint16),
        ("handle", c_uint16),
        ("count", c_uint16),
        ("length", c_uint16),
        #("value", list(AVAType)),
    ]

#class SetResult(BigEndianStructure):
#    _pack_ = 1
#    _fields_ = [
#        ("m_obj_class", c_uint16),
#        ("context_id", c_uint16),
#        ("handle", c_uint16),
#        ("attributeList", AttributeList),
#    ]


class MDSSetPriorityListResult(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),  # ro_type := RORS_APDU
        ("RORSapdu", RORSapdu),  # invoke_id := “mirrored from request message”,
        # command_type := CMD_CONFIRMED_SET
        ("SetResult", SetResult),  # managed_object := {NOM_MOC_VMS_MDS, 0, 0}
    ]

class NuObsValue(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("physio_id", c_uint16),
        ("state", c_uint16),
        # define INVALID 0x8000
        # define QUESTIONABLE 0x4000
        # define UNAVAILABLE 0x2000
        # define CALIBRATION_ONGOING 0x1000
        # define TEST_DATA 0x0800
        # define DEMO_DATA 0x0400
        # define VALIDATED_DATA 0x0080
        # define EARLY_INDICATION 0x0040
        # define MSMT_ONGOING 0x0020
        # define MSMT_STATE_IN_ALARM 0x0002
        # define MSMT_STATE_AL_INHIBITED 0x0001

        ("unit_code", c_uint16),
        ("value", c_float),
    ]


class SaObsValue(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("physio_id", c_uint16),
        ("state", c_uint16),
        ("length", c_uint16),
        #("value", list(c_uint8),
    ]


class VariableLabel(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("length", c_uint16),
        #("value", list(c_uint8),
    ]


class DispResolution(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("pre_point", c_uint8),
        ("post_point", c_uint8),
    ]

class NuObsValueCmp(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("count", c_uint16),
        ("length", c_uint16),
        # ("value", list(NuObsValue)),
    ]




class SystemLocal(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("text_catalog_revision", c_uint32),
        ("language", c_uint16),
        ("format", c_uint16),
    ]



class MdsGenSystemInfo(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("count", c_uint16),
        ("length", c_uint16),
        # ("value", list(MdsGenSystemInfoEntry)),
    ]



class SystemSpec(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("count", c_uint16),
        ("length", c_uint16),
        # ("value", list(SystemSpecEntry)),
    ]

class SystemSpecEntry(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("component_capab_id", c_uint16),
        ("length", c_uint16),
        # ("value", list(c_uint16)),
    ]



'''
typedef struct {
u_16 count;
u_16 length;
SystemSpecEntry value[1];
} SystemSpec;

typedef struct {
PrivateOid component_capab_id;
u_16 length;
u_16 value[1];
} SystemSpecEntry;
'''


"""
typedef struct
{
 u_16 count;
 u_16 length;
 MdsGenSystemInfoEntry value[1];
} MdsGenSystemInfo;
The MdsGenSysemInfoEntry allows to encode generic system information. It has the following
structure:
typedef struct
{
 u_16 choice;
#define MDS_GEN_SYSTEM_INFO_SYSTEM_PULSE_CHOSEN 1
 u_16 length;
 u_8 value[
"""








class MetricSpec(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("update_period", c_uint32),
        ("category", c_uint16),
        # define MCAT_UNSPEC 0
        # define AUTO_MEASUREMENT 1
        # define MANUAL_MEASUREMENT 2
        # define AUTO_SETTING 3
        # define MANUAL_SETTING 4
        # define AUTO_CALCULATION 5
        # define MANUAL_CALCULATION 6
        # define MULTI_DYNAMIC_CAPABILITIES 50
        # define AUTO_ADJUST_PAT_TEMP 128
        # define MANUAL_ADJUST_PAT_TEMP 129
        # define AUTO_ALARM_LIMIT_SETTING 130

        ("access", c_uint16),
        # define AVAIL_INTERMITTEND 0x8000
        # define UPD_PERIODIC 0x4000
        # define UPD_EPISODIC 0x2000
        # define MSMT_NONCONTINUOUS 0x1000


        # ("structure", MetricStructure),
        ("ms_struct", c_uint8),
        ("ms_comp_no", c_uint8),


        #typedef struct MetricStructure {
        # u_8 ms_struct;
        # u_8 ms_comp_no;
        #} MetricStructure;

        ("relevance", c_uint16),
    ]




# -----------------------------------------------------------------------------------------------------------------------


class BaseClass(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("FrameHdr", FrameHdr),
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),
    ]


# -----------------------------------------------------------------------------------------------------------------------

class BaseROIVapdu(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("FrameHdr", FrameHdr),
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),
        ("ROIVapdu", ROIVapdu),
    ]


# -----------------------------------------------------------------------------------------------------------------------


class BaseRORSapdu(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("FrameHdr", FrameHdr),
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),
        ("RORSapdu", RORSapdu),
    ]


class BaseRORSapdu_EventReportResult(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("FrameHdr", FrameHdr),
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),
        ("RORSapdu", RORSapdu),
        ("EventReportResult", EventReportResult),
    ]


class BaseRORSapdu_ActionResult(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("FrameHdr", FrameHdr),
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),
        ("RORSapdu", RORSapdu),
        ("ActionResult", ActionResult),
    ]


class BaseRORSapdu_ActionResult_PollMdibDataReplyExt(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("FrameHdr", FrameHdr),
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),
        ("RORSapdu", RORSapdu),
        ("ActionResult", ActionResult),
        ("PollMdibDataReplyExt", PollMdibDataReplyExt),
    ]


class BaseRORSapdu_GetResult(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("FrameHdr", FrameHdr),
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),
        ("RORSapdu", RORSapdu),
        ("GetResult", GetResult),
    ]


class BaseRORSapdu_SetResult(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("FrameHdr", FrameHdr),
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),
        ("RORSapdu", RORSapdu),
        ("SetResult", SetResult),
    ]


# -----------------------------------------------------------------------------------------------------------------------

class BaseROLRSapdu(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("FrameHdr", FrameHdr),
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),
        ("ROLRSapdu", ROLRSapdu),
    ]


# -----------------------------------------------------------------------------------------------------------------------

class BaseROERapdu(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("FrameHdr", FrameHdr),
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),
        ("ROERapdu", ROERapdu),
    ]

# -----------------------------------------------------------------------------------------------------------------------




class AssocReqSessionHeader(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("SessionHead", c_uint8),
        ("length", c_uint8),
    ]


class AssocReqUserData(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        # define MDDL_VERSION1 0x80000000
        ("ProtocolVersion", c_uint32),

        # define NOMEN_VERSION 0x40000000;
        ("NomenclatureVersion", c_uint32),

        ("FunctionalUnits", c_uint32),

        # define SYST_CLIENT 0x80000000
        # define SYST_SERVER 0x00800000
        ("SystemType", c_uint32),

        # define HOT_START 0x80000000
        # define WARM_START 0x40000000
        # define COLD_START 0x20000000
        ("StartupMode", c_uint32),

        ("AttributeList1", c_uint8),
        ("AttributeList2", c_uint8),
    ]


'''


# = Typedef ============================================================================================================

class RelativeTime(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("RelativeTime", c_uint32),
    ]


class OIDType(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("OIDType", c_uint16),
    ]


class MdsContext(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("MdsContext", c_uint16),
    ]


class Handle(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("Handle", c_uint16),
    ]


class ModifyOperator(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("ModifyOperator", c_uint16),
    ]


# = Basic Class ========================================================================================================

class FrameHdr(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("protocol_id", c_uint8),
        ("msg_type", c_uint8),
        ("length", c_uint16),
    ]


class AbsoluteTime(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("century", c_uint8),
        ("year", c_uint8),
        ("month", c_uint8),
        ("day", c_uint8),
        ("hour", c_uint8),
        ("minute", c_uint8),
        ("second", c_uint8),
        ("sec_fractions", c_uint8),
    ]


class SPpdu(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("session_id", c_uint16),  # contains a fixed value 0xE100
        ("p_context_id", c_uint16),  # negotiated in association phase, 2로 고정인듯?..
    ]


class ROapdus(BigEndianStructure):
    # define ROIV_APDU 1
    # define RORS_APDU 2
    # define ROER_APDU 3
    # define ROLRS_APDU 5
    _pack_ = 1
    _fields_ = [
        ("ro_type", c_uint16),  # ID for operation
        ("length", c_uint16),  # bytes to follow
    ]


class ROIVapdu(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("invoke_id", c_uint16),  # identifies the transaction
        ("command_type", c_uint16),  # identifies type of command
        ("length", c_uint16),  # no. of bytes in rest of message
    ]


class RORSapdu(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("invoke_id", c_uint16),  # mirrored back from op. invoke
        ("command_type", c_uint16),  # identifies type of command
        ("length", c_uint16),  # no. of bytes in rest of message
    ]


class RorlsId(BigEndianStructure):
    # define RORLS_FIRST 1 /* set in the first message */
    # define RORLS_NOT_FIRST_NOT_LAST 2
    # define RORLS_LAST 3 /* last RORLSapdu, one RORSapdu
    _pack_ = 1
    _fields_ = [
        ("state", c_uint8),
        ("count", c_uint8),  # counter starts with 1
    ]


class ROLRSapdu(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("linked_id", RorlsId),  # mirrored back from op. invoke
        ("invoke_id", c_uint16),  # mirrored back from op. invoke
        ("command_type", c_uint16),  # identifies type of command
        ("length", c_uint16),  # no. of bytes in rest of message
    ]


class ROERapdu(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("linked_id", RorlsId),
        ("error_value", c_uint16),
        ("length", c_uint16),
    ]


class GlbHandle(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("context_id", c_uint16),
        ("handle", c_uint16),
    ]


class ManagedObjectId(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_obj_class", c_uint16),
        ("m_obj_inst", GlbHandle),
    ]


class EventReportResult(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("managed_object", ManagedObjectId),  # mirrored from EvRep
        ("current_time", c_uint32),  # result time stamp
        ("event_type", c_uint16),  # identification of event
        ("length", c_uint16),  # size of appended data
    ]


class EventReportArgument(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("managed_object", ManagedObjectId),  # ident. of sender
        ("event_time", RelativeTime),  # event time stamp
        ("event_type", c_uint16),  # identification of event
        ("length", c_uint16),  # size of appended data
    ]




class AVAType(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("attribute_id", c_uint16),
        ("length", c_uint16),
        ("attribute_val", c_uint16),
    ]


#class AVAType(BigEndianStructure):
#    _pack_ = 1
#    _fields_ = [
#        ("attribute_id", OIDType),
#        ("length", c_uint16),
#        ("attribute_val", c_uint16),
#    ]



class AttributeList(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("count", c_uint16),
        ("length", c_uint16),
        # ("value", list(AVAType)),
    ]


class ConnectIndInfo(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("AttributeList", AttributeList),
    ]


class MdsCreateInfo(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("managed_object", ManagedObjectId),
        ("attribute_list", AttributeList),
    ]


# = Variable Class =====================================================================================================


# ======================================================================================================================


class Header_Common(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("FrameHdr", FrameHdr),
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),
    ]


# class MDSCreateEventResult(BigEndianStructure):
#    _pack_ = 1
#    _fields_ = [
#        ("FrameHdr", FrameHdr),
#        ("SPpdu", SPpdu),
#        ("ROapdus", ROapdus),
#        ("EventReportResult", EventReportResult),
#    ]


class ConnectIndication(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("Nomenclature", c_uint32),
        ("ROapdus", ROapdus),                           # ro_type := ROIVapdu
        ("ROIVapdu", ROIVapdu),                         # command_type := CMD_EVENT_REPORT
        ("EventReportArgument", EventReportArgument),   # managed_object:={NOM_MOC_MDS_COMPOS_SINGLE_BED,0,0
                                                        # event_type := NOM_NOTI_MDS_CONNECT_INDIC
        ("ConnectIndInfo", ConnectIndInfo),
    ]


class MDSCreateEventReport(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),  # ro_type := ROIV_APDU
        ("ROIVapdu", ROIVapdu),  # command_type := CMD_CONFIRMED_EVENT_REPORT
        ("EventReportArgument", EventReportArgument),  # managed_object:={NOM_MOC_VMS_MDS,0,0
        # event_type := NOM_NOTI_MDS_CREAT
        ("MDSCreateInfo", MdsCreateInfo),
    ]


class MDSCreateEventResult(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),  # ro_type := RORS_APDU
        ("RORSapdu", RORSapdu),  # invoke_id := mirrored from event report
        # command_type := CMD_CONFIRMED_EVENT_REPORT
        ("EventReportResult", EventReportResult),  # managed_object := mirrored from event report
        # event_type := NOM_NOTI_MDS_CREAT
        # length := 0
    ]


# define NOM_ACT_POLL_MDIB_DATA 3094
# define NOM_ACT_POLL_MDIB_DATA_EXT 61755

class ActionArgument(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("managed_object", ManagedObjectId),  # addressed object
        ("scope", c_uint32),  # fixed value 0
        ("action_type", OIDType),  # identification of method

        ("length", c_uint16),  # size of appended data
    ]


# define NOM_PART_OBJ 1
# define NOM_PART_SCADA 2
# define NOM_PART_EVT 3
# define NOM_PART_DIM 4
# define NOM_PART_PGRP 6
# define NOM_PART_INFRASTRUCT 8

class NomPartition(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("NomPartition", c_uint16),
    ]


class TYPE(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("partition", NomPartition),
        ("code", OIDType),
    ]


class PollMdibDataReq(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("poll_number", c_uint16),
        ("polled_obj_type", TYPE),
        ("polled_attr_grp", OIDType),
    ]


class MDSPollAction(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),  # ro_type := ROIV_APDU
        ("ROIVapdu", ROIVapdu),  # command_type := CMD_CONFIRMED_ACTION

        ("ActionArgument", ActionArgument),  # managed_object := {NOM_MOC_VMS_MDS, 0, 0}
        # action_type := NOM_ACT_POLL_MDIB_DATA
        ("PollMdibDataReq", PollMdibDataReq),

    ]


class ActionResult(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("managed_object", ManagedObjectId),
        ("action_type", OIDType),  # identification of method
        ("length", c_uint16),  # size of appended data
    ]


class ObservationPoll(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("obj_handle", c_uint16),
        ("count", c_uint16),
        ("length", c_uint16),
        #("value", list(AVAType)),  # identification of method
    ]


#class ObservationPoll(BigEndianStructure):
#    _pack_ = 1
#    _fields_ = [
#        ("obj_handle", Handle),
#        ("attributes", AttributeList),  # identification of method
#    ]


class poll_info(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("count", c_uint16),
        ("length", c_uint16),
        # ("value", list(ObservationPoll)),
    ]


class SingleContextPoll(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("context_id", c_uint16),
        ("count", c_uint16),
        ("length", c_uint16),
        # ("value", list(ObservationPoll)),
    ]

#class SingleContextPoll(BigEndianStructure):
#    _pack_ = 1
#    _fields_ = [
#        ("context_id", MdsContext),
#        ("poll_info", poll_info),
#    ]


class PollInfoList(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("count", c_uint16),
        ("length", c_uint16),
        # ("value", list(SingleContextPoll)),
    ]


class PollMdibDataReply(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("poll_number", c_uint16),
        ("rel_time_stamp", RelativeTime),
        ("abs_time_stamp", AbsoluteTime),
        ("polled_obj_type", TYPE),
        ("polled_attr_grp", OIDType),
        ("poll_info_list", PollInfoList),
    ]


class MDSPollActionResult(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),  # ro_type := RORS_APDU
        ("RORSapdu", RORSapdu),  # invoke_id := "mirrored from request message"
        # command_type := CMD_CONFIRMED_ACTION

        ("ActionResult", ActionResult),  # managed_object := {NOM_MOC_VMS_MDS, 0, 0}
        # action_type := NOM_ACT_POLL_MDIB_DATA
        # ("PollMdibDataReply", PollMdibDataReply),
    ]


class PollMdibDataReqExt(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("poll_number", c_uint16),
        ("polled_obj_type", TYPE),
        ("polled_attr_grp", OIDType),
        ("poll_ext_attr", AttributeList),
    ]


class MDSPollAction(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),  # ro_type := RORS_APDU
        ("ROIVapdu", ROIVapdu),  # command_type := CMD_CONFIRMED_ACTION
        ("ActionArgument", ActionArgument),  # managed_object := {NOM_MOC_VMS_MDS, 0, 0}
        # action_type := NOM_ACT_POLL_MDIB_DATA_EXT
        ("PollMdibDataReqExt", PollMdibDataReqExt),

    ]


class PollMdibDataReplyExt(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("poll_number", c_uint16),
        ("sequence_no", c_uint16),
        ("rel_time_stamp", RelativeTime),
        ("abs_time_stamp", AbsoluteTime),
        ("polled_obj_type", TYPE),
        ("polled_attr_grp", OIDType),
        ("poll_info_list", PollInfoList),

    ]


class MDSPollActionResultExt(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),  # ro_type := RORS_APDU
        ("RORSapdu", RORSapdu),  # invoke_id := "mirrored from request message"
        # command_type := CMD_CONFIRMED_ACTION
        ("ActionResult", ActionResult),  # managed_object := {NOM_MOC_VMS_MDS, 0, 0}
        # action_type := NOM_ACT_POLL_MDIB_DATA_EXT
        # ("PollMdibDataReplyExt", PollMdibDataReplyExt),

    ]


class AttributeIdList(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("count", c_uint16),
        ("length", c_uint16),
        ("attributeIdList", c_uint16),
        # ("attributeIdList", list(OIDType)),
    ]


class GetArgument(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("managed_object", ManagedObjectId),
        ("scope", c_uint32),
        ("attributeIdList", AttributeIdList),
    ]


class MDSGetPriorityList(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),  # ro_type := ROIV_APDU
        ("ROIVapdu", ROIVapdu),  # command_type := CMD_GET
        ("GetArgument", GetArgument),  # managed_object := {NOM_MOC_VMS_MDS, 0, 0}
    ]


class GetResult(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("managed_object", ManagedObjectId),
        ("attributeList", AttributeList),
    ]


class MDSGetPriorityListResult(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),  # ro_type := RORS_APDU
        ("RORSapdu", RORSapdu),  # invoke_id := “mirrored from request message”,
        # command_type := CMD_GET
        ("GetResult", GetResult),  # managed_object := {NOM_MOC_VMS_MDS, 0, 0}
    ]


class AttributeModEntry(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("modifyOperator", ModifyOperator),
        ("attribute", AVAType),
    ]


class ModificationList(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("count", c_uint16),
        ("length", c_uint16),
        # ("value", list(AttributeModEntry)),
    ]


class SetArgument(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("managed_object", ManagedObjectId),
        ("ROapdus", c_uint32),
        ("modificationList", ModificationList),
    ]


class MDSSetPriorityList(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),  # ro_type := RORS_APDU
        ("ROIVapdu", ROIVapdu),  # invoke_id := “mirrored from request message”,
        # command_type := CMD_GET
        ("SetArgument", SetArgument),  # managed_object := {NOM_MOC_VMS_MDS, 0, 0}
    ]


class SetResult(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("managed_object", ManagedObjectId),
        ("attributeList", AttributeList),
    ]


class MDSSetPriorityListResult(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),  # ro_type := RORS_APDU
        ("RORSapdu", RORSapdu),  # invoke_id := “mirrored from request message”,
        # command_type := CMD_CONFIRMED_SET
        ("SetResult", SetResult),  # managed_object := {NOM_MOC_VMS_MDS, 0, 0}
    ]


# -----------------------------------------------------------------------------------------------------------------------


class BaseClass(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("FrameHdr", FrameHdr),
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),
    ]


# -----------------------------------------------------------------------------------------------------------------------

class BaseROIVapdu(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("FrameHdr", FrameHdr),
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),
        ("ROIVapdu", ROIVapdu),
    ]


# -----------------------------------------------------------------------------------------------------------------------


class BaseRORSapdu(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("FrameHdr", FrameHdr),
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),
        ("RORSapdu", RORSapdu),
    ]


class BaseRORSapdu_EventReportResult(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("FrameHdr", FrameHdr),
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),
        ("RORSapdu", RORSapdu),
        ("EventReportResult", EventReportResult),
    ]


class BaseRORSapdu_ActionResult(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("FrameHdr", FrameHdr),
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),
        ("RORSapdu", RORSapdu),
        ("ActionResult", ActionResult),
    ]


class BaseRORSapdu_ActionResult_PollMdibDataReplyExt(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("FrameHdr", FrameHdr),
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),
        ("RORSapdu", RORSapdu),
        ("ActionResult", ActionResult),
        ("PollMdibDataReplyExt", PollMdibDataReplyExt),
    ]


class BaseRORSapdu_GetResult(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("FrameHdr", FrameHdr),
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),
        ("RORSapdu", RORSapdu),
        ("GetResult", GetResult),
    ]


class BaseRORSapdu_SetResult(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("FrameHdr", FrameHdr),
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),
        ("RORSapdu", RORSapdu),
        ("SetResult", SetResult),
    ]


# -----------------------------------------------------------------------------------------------------------------------

class BaseROLRSapdu(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("FrameHdr", FrameHdr),
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),
        ("ROLRSapdu", ROLRSapdu),
    ]


# -----------------------------------------------------------------------------------------------------------------------

class BaseROERapdu(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("FrameHdr", FrameHdr),
        ("SPpdu", SPpdu),
        ("ROapdus", ROapdus),
        ("ROERapdu", ROERapdu),
    ]

# -----------------------------------------------------------------------------------------------------------------------

'''