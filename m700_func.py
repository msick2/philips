import m700_struct
import sys
import ctypes


def l0_FrameHdr(array_data):
    dict_ret = dict()
    dict_data = dict()

    obj = m700_struct.FrameHdr.from_buffer(array_data)

    dict_data['protocol_id'] = obj.protocol_id
    dict_data['msg_type'] = obj.msg_type
    dict_data['length'] = obj.length

    dict_ret['FrameHdr'] = dict_data
    dict_ret['tail'] = array_data[ctypes.sizeof(obj):len(array_data)]
    dict_ret['orn'] = array_data

    return dict_ret


def l1_SPpdu(dict_ret):
    dict_data = dict()
    array_data = dict_ret['tail']

    obj = m700_struct.SPpdu.from_buffer(array_data)

    dict_data['session_id'] = obj.session_id
    dict_data['p_context_id'] = obj.p_context_id

    dict_ret['SPpdu'] = dict_data
    dict_ret['tail'] = array_data[ctypes.sizeof(obj):len(array_data)]

    return dict_ret


def l1_ROapdus(dict_ret):
    dict_data = dict()
    array_data = dict_ret['tail']

    obj = m700_struct.ROapdus.from_buffer(array_data)

    dict_data['ro_type'] = obj.ro_type
    dict_data['length'] = obj.length

    dict_ret['ROapdus'] = dict_data
    dict_ret['tail'] = array_data[ctypes.sizeof(obj):len(array_data)]

    return dict_ret





def l2_ROIVapdu(dict_ret):
    dict_data = dict()
    array_data = dict_ret['tail']

    obj = m700_struct.ROIVapdu.from_buffer(array_data)

    dict_data['invoke_id'] = obj.invoke_id
    dict_data['command_type'] = obj.command_type
    dict_data['length'] = obj.length

    dict_ret['ROIVapdu'] = dict_data
    dict_ret['tail'] = array_data[ctypes.sizeof(obj):len(array_data)]

    return dict_ret


def l3_EventReportArgument(dict_ret):
    dict_data = dict()
    array_data = dict_ret['tail']

    obj = m700_struct.EventReportArgument.from_buffer(array_data)

    dict_data['managed_object'] = obj.managed_object
    dict_data['event_time'] = obj.event_time
    dict_data['event_type'] = obj.event_type
    dict_data['length'] = obj.length

    dict_ret['EventReportArgument'] = dict_data
    dict_ret['tail'] = array_data[ctypes.sizeof(obj):len(array_data)]

    return dict_ret


def l2_RORSapdu(dict_ret):
    dict_data = dict()
    array_data = dict_ret['tail']

    obj = m700_struct.ROIVapdu.from_buffer(array_data)

    dict_data['invoke_id'] = obj.invoke_id
    dict_data['command_type'] = obj.command_type
    dict_data['length'] = obj.length

    dict_ret['RORSapdu'] = dict_data
    dict_ret['tail'] = array_data[ctypes.sizeof(obj):len(array_data)]

    return dict_ret


def l3_EventReportResult(dict_ret):
    dict_data = dict()
    array_data = dict_ret['tail']

    obj = m700_struct.EventReportResult.from_buffer(array_data)

    dict_data['managed_object'] = obj.managed_object
    dict_data['current_time'] = obj.current_time
    dict_data['event_type'] = obj.event_type
    dict_data['length'] = obj.length

    dict_ret['EventReportResult'] = dict_data
    dict_ret['tail'] = array_data[ctypes.sizeof(obj):len(array_data)]

    return dict_ret


def l4_ActionResult(dict_ret):
    dict_data = dict()
    array_data = dict_ret['tail']

    obj = m700_struct.ActionResult.from_buffer(array_data)

    dict_data['managed_object'] = obj.managed_object
    dict_data['action_type'] = obj.action_type
    dict_data['length'] = obj.length

    dict_ret['ActionResult'] = dict_data
    dict_ret['tail'] = array_data[ctypes.sizeof(obj):len(array_data)]

    return dict_ret


def l5_PollMdibDataReply(dict_ret):
    dict_data = dict()
    array_data = dict_ret['tail']

    obj = m700_struct.PollMdibDataReply.from_buffer(array_data)

    dict_data['poll_number'] = obj.poll_number
    dict_data['rel_time_stamp'] = obj.rel_time_stamp
    dict_data['abs_time_stamp'] = obj.abs_time_stamp
    dict_data['polled_obj_type'] = obj.polled_obj_type
    dict_data['polled_attr_grp'] = obj.polled_attr_grp
    dict_data['poll_info_list'] = obj.poll_info_list

    dict_ret['PollMdibDataReply'] = dict_data
    dict_ret['tail'] = array_data[ctypes.sizeof(obj):len(array_data)]

    return dict_ret




def base_decode(array_data):
    obj = m700_struct.BaseClass.from_buffer(array_data)
    dict_ret = dict()
    dict_ret['obj'] = obj
    dict_ret['tail'] = array_data[ctypes.sizeof(obj):len(array_data)]
    dict_ret['orn'] = array_data

    return dict_ret














































