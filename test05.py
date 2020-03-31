import ctypes

import m700_struct
import rcv_data_restore
import data_computer
import data_monitor
import json


class Parser:

    def __init__(self):
        #    self.file_print = open("file_print.txt", "w")
        pass

    def __del__(self):
        #    self.file_print.close()
        pass

    # ==================================================================================================================
    def decoding(self, base_class, byte_array_data):
        obj = base_class.from_buffer(byte_array_data)

        dict_ret = \
            {
                'obj': obj,
                'tail': byte_array_data[ctypes.sizeof(obj):len(byte_array_data)],
            }

        return dict_ret

    # ==================================================================================================================

    def input_data(self, data_bytearray):
        ret_dict = dict()
        data_FrameHdr = self.decoding(m700_struct.FrameHdr, data_bytearray)
        data_SPpdu = self.decoding(m700_struct.SPpdu, data_FrameHdr['tail'])
        data_ROapdus = self.decoding(m700_struct.ROapdus, data_SPpdu['tail'])

        ret_dict['FrameHdr'] = dict()
        ret_dict['FrameHdr']['protocol_id'] = data_FrameHdr['obj'].protocol_id
        ret_dict['FrameHdr']['msg_type'] = data_FrameHdr['obj'].msg_type
        ret_dict['FrameHdr']['length'] = data_FrameHdr['obj'].length

        ret_dict['SPpdu'] = dict()
        ret_dict['SPpdu']['session_id'] = data_SPpdu['obj'].session_id
        ret_dict['SPpdu']['p_context_id'] = data_SPpdu['obj'].p_context_id

        ret_dict['ROapdus'] = dict()
        ret_dict['ROapdus']['ro_type'] = data_ROapdus['obj'].ro_type
        ret_dict['ROapdus']['length'] = data_ROapdus['obj'].length

        # = 1. ROIV_APDU ===========================================================
        if data_ROapdus['obj'].ro_type == m700_struct.ROIV_APDU:
            data_ROIVapdu = self.decoding(m700_struct.ROIVapdu, data_ROapdus['tail'])

            ret_dict['ROIVapdu'] = dict()
            ret_dict['ROIVapdu']['invoke_id'] = data_ROIVapdu['obj'].invoke_id
            ret_dict['ROIVapdu']['command_type'] = data_ROIVapdu['obj'].command_type
            ret_dict['ROIVapdu']['length'] = data_ROIVapdu['obj'].length



        # = 1. RORS_APDU ===========================================================
        elif data_ROapdus['obj'].ro_type == m700_struct.RORS_APDU:
            data_RORSapdu = self.decoding(m700_struct.RORSapdu, data_ROapdus['tail'])

            ret_dict['RORSapdu'] = dict()
            ret_dict['RORSapdu']['invoke_id'] = data_RORSapdu['obj'].invoke_id
            ret_dict['RORSapdu']['command_type'] = data_RORSapdu['obj'].command_type
            ret_dict['RORSapdu']['length'] = data_RORSapdu['obj'].length

            # = 2. CMD_CONFIRMED_EVENT_REPORT =====================================
            if data_RORSapdu['obj'].command_type == m700_struct.CMD_CONFIRMED_EVENT_REPORT:
                data_EventReportResult = self.decoding(m700_struct.EventReportResult, data_RORSapdu['tail'])

                ret_dict['EventReportResult'] = dict()
                ret_dict['EventReportResult']['m_obj_class'] = data_EventReportResult['obj'].m_obj_class
                ret_dict['EventReportResult']['context_id'] = data_EventReportResult['obj'].context_id
                ret_dict['EventReportResult']['handle'] = data_EventReportResult['obj'].handle
                ret_dict['EventReportResult']['current_time'] = data_EventReportResult['obj'].current_time
                ret_dict['EventReportResult']['event_type'] = data_EventReportResult['obj'].event_type
                ret_dict['EventReportResult']['length'] = data_EventReportResult['obj'].length

            # = 2. CMD_CONFIRMED_ACTION ===========================================
            elif data_RORSapdu['obj'].command_type == m700_struct.CMD_CONFIRMED_ACTION:
                data_ActionResult = self.decoding(m700_struct.ActionResult, data_RORSapdu['tail'])

                ret_dict['ActionResult'] = dict()
                ret_dict['ActionResult']['m_obj_class'] = data_ActionResult['obj'].m_obj_class
                ret_dict['ActionResult']['context_id'] = data_ActionResult['obj'].context_id
                ret_dict['ActionResult']['handle'] = data_ActionResult['obj'].handle
                ret_dict['ActionResult']['action_type'] = data_ActionResult['obj'].action_type
                ret_dict['ActionResult']['length'] = data_ActionResult['obj'].length

                if data_ActionResult['obj'].action_type == m700_struct.NOM_ACT_POLL_MDIB_DATA:
                    data_PollMdibDataReply = self.decoding(m700_struct.PollMdibDataReply, data_ActionResult['tail'])

                    ret_dict['PollMdibDataReply'] = dict()
                    ret_dict['PollMdibDataReply']['poll_number'] = data_PollMdibDataReply['obj'].poll_number
                    ret_dict['PollMdibDataReply']['rel_time_stamp'] = data_PollMdibDataReply['obj'].rel_time_stamp
                    ret_dict['PollMdibDataReply']['century'] = data_PollMdibDataReply['obj'].century
                    ret_dict['PollMdibDataReply']['year'] = data_PollMdibDataReply['obj'].year
                    ret_dict['PollMdibDataReply']['month'] = data_PollMdibDataReply['obj'].month
                    ret_dict['PollMdibDataReply']['day'] = data_PollMdibDataReply['obj'].day
                    ret_dict['PollMdibDataReply']['hour'] = data_PollMdibDataReply['obj'].hour
                    ret_dict['PollMdibDataReply']['minute'] = data_PollMdibDataReply['obj'].minute
                    ret_dict['PollMdibDataReply']['second'] = data_PollMdibDataReply['obj'].second
                    ret_dict['PollMdibDataReply']['sec_fractions'] = data_PollMdibDataReply['obj'].sec_fractions
                    ret_dict['PollMdibDataReply']['partition'] = data_PollMdibDataReply['obj'].partition
                    ret_dict['PollMdibDataReply']['code'] = data_PollMdibDataReply['obj'].code
                    ret_dict['PollMdibDataReply']['polled_attr_grp'] = data_PollMdibDataReply['obj'].polled_attr_grp
                    # ret_dict['PollMdibDataReply']['poll_info_list'] = data_PollMdibDataReply['obj'].poll_info_list

                    ret_dict['PollMdibDataReply']['poll_info_list'] = dict()

                    data_PollInfoList = self.decoding(m700_struct.PollInfoList, data_PollMdibDataReply['tail'])
                    tail = data_PollInfoList['tail']

                    ret_dict['PollMdibDataReply']['poll_info_list']['count'] = data_PollInfoList['obj'].count
                    ret_dict['PollMdibDataReply']['poll_info_list']['length'] = data_PollInfoList['obj'].length
                    ret_dict['PollMdibDataReply']['poll_info_list']['value'] = list(m700_struct.SingleContextPoll)[
                        data_PollInfoList['obj'].count]

                    # ("value", list(SingleContextPoll)),

                    for _ in range(data_PollInfoList['obj'].count):

                        data_SingleContextPoll = self.decoding(m700_struct.SingleContextPoll, tail)
                        tail = data_SingleContextPoll['tail']

                        # ("value", list(ObservationPoll)),

                        for _ in range(data_SingleContextPoll['obj'].count):
                            data_ObservationPoll = self.decoding(m700_struct.ObservationPoll, tail)
                            tail = data_ObservationPoll['tail']
                            # ("value", list(AVAType)),

                            for _ in range(data_ObservationPoll['obj'].count):
                                data_AVAType = self.decoding(m700_struct.AVAType, tail)
                                tail = data_AVAType['tail']
                                data = tail[0: data_AVAType['obj'].length]
                                # print(f"| data_AVAType.attribute_val   : {data_AVAType['obj'].attribute_val}")
                                self.file_log_1.write(f"| Data: [{len(data)}] - {data}\n")

                                self.decode_func(data_AVAType['obj'].attribute_id, data_AVAType['obj'].length, data)

                                tail = tail[data_AVAType['obj'].length:len(tail)]




                elif data_ActionResult['obj'].action_type == m700_struct.NOM_ACT_POLL_MDIB_DATA_EXT:
                    data_PollMdibDataReplyExt = self.decoding(m700_struct.PollMdibDataReplyExt,
                                                              data_ActionResult['tail'])

                    ret_dict['PollMdibDataReplyExt'] = dict()
                    ret_dict['PollMdibDataReplyExt']['poll_number'] = data_PollMdibDataReplyExt['obj'].poll_number
                    ret_dict['PollMdibDataReplyExt']['sequence_no'] = data_PollMdibDataReplyExt['obj'].sequence_no
                    ret_dict['PollMdibDataReplyExt']['rel_time_stamp'] = data_PollMdibDataReplyExt['obj'].rel_time_stamp
                    ret_dict['PollMdibDataReplyExt']['century'] = data_PollMdibDataReplyExt['obj'].century
                    ret_dict['PollMdibDataReplyExt']['year'] = data_PollMdibDataReplyExt['obj'].year
                    ret_dict['PollMdibDataReplyExt']['month'] = data_PollMdibDataReplyExt['obj'].month
                    ret_dict['PollMdibDataReplyExt']['day'] = data_PollMdibDataReplyExt['obj'].day
                    ret_dict['PollMdibDataReplyExt']['hour'] = data_PollMdibDataReplyExt['obj'].hour
                    ret_dict['PollMdibDataReplyExt']['minute'] = data_PollMdibDataReplyExt['obj'].minute
                    ret_dict['PollMdibDataReplyExt']['second'] = data_PollMdibDataReplyExt['obj'].second
                    ret_dict['PollMdibDataReplyExt']['sec_fractions'] = data_PollMdibDataReplyExt['obj'].sec_fractions
                    ret_dict['PollMdibDataReplyExt']['partition'] = data_PollMdibDataReplyExt['obj'].partition
                    ret_dict['PollMdibDataReplyExt']['code'] = data_PollMdibDataReplyExt['obj'].code
                    ret_dict['PollMdibDataReplyExt']['polled_attr_grp'] = data_PollMdibDataReplyExt[
                        'obj'].polled_attr_grp
                    # ret_dict['PollMdibDataReply']['poll_info_list'] = data_PollMdibDataReplyExt['obj'].poll_info_list

                    ret_dict['PollMdibDataReplyExt']['poll_info_list'] = dict()

                    data_PollInfoList = self.decoding(m700_struct.PollInfoList, data_PollMdibDataReplyExt['tail'])
                    tail = data_PollInfoList['tail']

                    ret_dict['PollMdibDataReplyExt']['poll_info_list']['count'] = data_PollInfoList['obj'].count
                    ret_dict['PollMdibDataReplyExt']['poll_info_list']['length'] = data_PollInfoList['obj'].length
                    ret_dict['PollMdibDataReplyExt']['poll_info_list']['value_list'] = list()

                    for _ in range(data_PollInfoList['obj'].count):

                        data_SingleContextPoll = self.decoding(m700_struct.SingleContextPoll, tail)
                        tail = data_SingleContextPoll['tail']

                        dict_SingleContextPoll_append = dict()

                        dict_SingleContextPoll_append['context_id'] = data_SingleContextPoll['obj'].context_id
                        dict_SingleContextPoll_append['count'] = data_SingleContextPoll['obj'].count
                        dict_SingleContextPoll_append['length'] = data_SingleContextPoll['obj'].length
                        dict_SingleContextPoll_append['value_list'] = list()

                        for _ in range(data_SingleContextPoll['obj'].count):
                            data_ObservationPoll = self.decoding(m700_struct.ObservationPoll, tail)
                            tail = data_ObservationPoll['tail']

                            dict_ObservationPoll_append = dict()
                            dict_ObservationPoll_append['obj_handle'] = data_ObservationPoll['obj'].obj_handle
                            dict_ObservationPoll_append['count'] = data_ObservationPoll['obj'].count
                            dict_ObservationPoll_append['length'] = data_ObservationPoll['obj'].length
                            dict_ObservationPoll_append['value_list'] = list()

                            for _ in range(data_ObservationPoll['obj'].count):
                                data_AVAType = self.decoding(m700_struct.AVAType, tail)
                                tail = data_AVAType['tail']
                                data = tail[0: data_AVAType['obj'].length]

                                dict_AVAType_append = dict()
                                dict_AVAType_append['attribute_id'] = data_AVAType['obj'].attribute_id
                                dict_AVAType_append['length'] = data_AVAType['obj'].length
                                # dict_AVAType_append['datalength'] = len(data)

                                dict_AVAType_append['data'] = self.decode_attribute \
                                        (
                                        data_AVAType['obj'].attribute_id,
                                        data_AVAType['obj'].length,
                                        data
                                    )

                                tail = tail[data_AVAType['obj'].length:len(tail)]

                                dict_ObservationPoll_append['value_list'].append(dict_AVAType_append)

                            dict_SingleContextPoll_append['value_list'].append(dict_ObservationPoll_append)

                        ret_dict['PollMdibDataReplyExt']['poll_info_list']['value_list'].append(
                            dict_SingleContextPoll_append)

            # = 2. CMD_GET =======================================================
            elif data_RORSapdu['obj'].command_type == m700_struct.CMD_GET:
                data_GetResult = self.decoding(m700_struct.GetResult, data_RORSapdu['tail'])

                ret_dict['GetResult'] = dict()
                ret_dict['GetResult']['m_obj_class'] = data_GetResult['obj'].m_obj_class
                ret_dict['GetResult']['context_id'] = data_GetResult['obj'].context_id
                ret_dict['GetResult']['handle'] = data_GetResult['obj'].handle
                # ret_dict['GetResult']['attributeList'] = data_GetResult['obj'].attributeList

            # = 2. CMD_CONFIRMED_SET =============================================
            elif data_RORSapdu['obj'].command_type == m700_struct.CMD_CONFIRMED_SET:
                data_SetResult = self.decoding(m700_struct.SetResult, data_RORSapdu['tail'])

                ret_dict['SetResult'] = dict()
                ret_dict['SetResult']['m_obj_class'] = data_SetResult['obj'].m_obj_class
                ret_dict['SetResult']['context_id'] = data_SetResult['obj'].context_id
                ret_dict['SetResult']['handle'] = data_SetResult['obj'].handle
                ret_dict['SetResult']['count'] = data_SetResult['obj'].count
                ret_dict['SetResult']['length'] = data_SetResult['obj'].length
                # ret_dict['SetResult']['attributeList'] = data_SetResult['obj'].attributeList

        return ret_dict

    def decode_attribute(self, attribute_id, length, data_array):
        ret_dict = dict()

        if attribute_id == m700_struct.NOM_ATTR_SA_VAL_OBS:

            data_obj = self.decoding(m700_struct.SaObsValue, data_array)
            ret_dict['physio_id'] = data_obj['obj'].physio_id
            ret_dict['state'] = data_obj['obj'].state
            ret_dict['length'] = data_obj['obj'].length
            ret_dict['data_list'] = self.decode_byte_data(data_obj['tail'])

        elif attribute_id == m700_struct.NOM_ATTR_NU_VAL_OBS:
            data_obj = self.decoding(m700_struct.NuObsValue, data_array)

            ret_dict['physio_id'] = data_obj['obj'].physio_id
            ret_dict['state'] = data_obj['obj'].state
            ret_dict['unit_code'] = data_obj['obj'].unit_code
            ret_dict['value'] = data_obj['obj'].value

        elif attribute_id == m700_struct.NOM_ATTR_TIME_STAMP_ABS:
            data_obj = self.decoding(m700_struct.AbsoluteTime, data_array)

            ret_dict['century'] = data_obj['obj'].century
            ret_dict['year'] = data_obj['obj'].year
            ret_dict['month'] = data_obj['obj'].month
            ret_dict['day'] = data_obj['obj'].day
            ret_dict['hour'] = data_obj['obj'].hour
            ret_dict['minute'] = data_obj['obj'].minute
            ret_dict['second'] = data_obj['obj'].second
            ret_dict['sec_fractions'] = data_obj['obj'].sec_fractions

        elif attribute_id == m700_struct.NOM_ATTR_NU_CMPD_VAL_OBS:
            data_obj = self.decoding(m700_struct.NuObsValueCmp, data_array)
            ret_dict['count'] = data_obj['obj'].count
            ret_dict['length'] = data_obj['obj'].length
            ret_dict['data_list'] = list()
            # print(data_obj['tail'])

            tail = data_obj['tail']

            for _ in range(data_obj['obj'].count):
                dict_res = dict()
                data_obj = self.decoding(m700_struct.NuObsValue, tail)
                dict_res['physio_id'] = data_obj['obj'].physio_id
                dict_res['state'] = data_obj['obj'].state
                dict_res['unit_code'] = data_obj['obj'].unit_code
                dict_res['value'] = data_obj['obj'].value
                ret_dict['data_list'].append(dict_res)


        elif attribute_id == m700_struct.NOM_ATTR_TIME_STAMP_REL:
            data_obj = self.decoding(m700_struct.RelativeTime, data_array)
            ret_dict['RelativeTime'] = data_obj['obj'].RelativeTime

        return ret_dict

    def decode_byte_data(self, data_array):
        ret_list = list()

        front = 0
        flag_ = 0
        for byte_data in data_array:
            if flag_ == 0:
                front = byte_data * 256
                flag_ = 1
            else:
                flag_ = 0
                ret_list.append(front + byte_data)

        return ret_list

    def decode_float_data(self, data_array):
        ret_list = list()
        count = int(len(data_array) / 4)

        # print(len(data_array))

        for _ in range(count):
            data_obj = self.decoding(m700_struct.FLOAT, data_array)
            ret_list.append(data_obj['obj'].data)
            data_array = data_obj['tail']
            # print(data_obj['data'])

        return ret_list


def print_dict(data_dict):
    print(len(data_dict))

    for data in data_dict:

        if data == 'FrameHdr':
            print(f"FrameHdr.protocol_id = {data_dict[data].protocol_id}")
            print(f"FrameHdr.msg_type    = {data_dict[data].msg_type}")
            print(f"FrameHdr.length      = {data_dict[data].length}")

        elif data == 'SPpdu':
            print(f"SPpdu.session_id     = {data_dict[data].session_id}")
            print(f"SPpdu.p_context_id   = {data_dict[data].p_context_id}")

        elif data == 'ROapdus':
            print(f"ROapdus.ro_type      = {data_dict[data].ro_type}")
            print(f"ROapdus.length       = {data_dict[data].length}")

        # if len(data_dict[data]) > 0:
        #    print_dict(data_dict[data])


cParser = Parser()

ok = 0
nok = 1

index = 0

# res = rcv_data_restore.input_rcv_data(data_monitor.datas4[4997])
# cParser.get_data(res[1])

file_print = open("file_print.txt", "w")

for data in data_monitor.datas4:
    # for data in data_computer.datas1:

    res = rcv_data_restore.input_rcv_data(data)

    if res[0]:
        ok += 1

        data_dict = cParser.input_data(res[1])
        # print( json.dumps(data_dict))
        # print_dict(data_dict)
        # print(data_dict['FrameHdr'].protocol_id)
        file_print.write(f"{json.dumps(data_dict)}\n")


    else:
        # print(res[1])
        nok += 1

    index += 1

file_print.close()
