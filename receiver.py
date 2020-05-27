import ctypes

import philips_struct
import philips_constants
import rcv_data_restore
import data_computer
import data_monitor
import json


class Parser:

    # ==================================================================================================================
    def decoding(self, base_class, byte_array_data):
        obj = base_class.from_buffer(byte_array_data)

        dict_ret = \
            {
                'obj': obj,
                'tail': byte_array_data[ctypes.sizeof(obj):len(byte_array_data)],
            }

        return dict_ret

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
            data_obj = self.decoding(philips_struct.FLOAT, data_array)
            ret_list.append(data_obj['obj'].data)
            data_array = data_obj['tail']
            # print(data_obj['data'])

        return ret_list

    # ==================================================================================================================

    def input_data(self, data_bytearray):
        ret_dict = dict()
        data_FrameHdr = self.decoding(philips_struct.FrameHdr, data_bytearray)
        data_SPpdu = self.decoding(philips_struct.SPpdu, data_FrameHdr['tail'])
        data_ROapdus = self.decoding(philips_struct.ROapdus, data_SPpdu['tail'])

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
        if data_ROapdus['obj'].ro_type == philips_constants.ROIV_APDU:
            data_ROIVapdu = self.decoding(philips_struct.ROIVapdu, data_ROapdus['tail'])

            ret_dict['ROIVapdu'] = dict()
            ret_dict['ROIVapdu']['invoke_id'] = data_ROIVapdu['obj'].invoke_id
            ret_dict['ROIVapdu']['command_type'] = data_ROIVapdu['obj'].command_type
            ret_dict['ROIVapdu']['length'] = data_ROIVapdu['obj'].length

            # = 2. CMD_CONFIRMED_EVENT_REPORT =====================================
            if data_ROIVapdu['obj'].command_type == philips_constants.CMD_CONFIRMED_EVENT_REPORT:

                data_EventReportArgument = self.decoding(philips_struct.EventReportArgument, data_ROIVapdu['tail'])
                ret_dict['EventReportArgument'] = dict()
                ret_dict['EventReportArgument']['m_obj_class'] = data_EventReportArgument['obj'].m_obj_class
                ret_dict['EventReportArgument']['context_id'] = data_EventReportArgument['obj'].context_id
                ret_dict['EventReportArgument']['handle'] = data_EventReportArgument['obj'].handle
                ret_dict['EventReportArgument']['event_time'] = data_EventReportArgument['obj'].event_time
                ret_dict['EventReportArgument']['event_type'] = data_EventReportArgument['obj'].event_type
                ret_dict['EventReportArgument']['length'] = data_EventReportArgument['obj'].length

                # = 3. NOM_NOTI_MDS_CREAT =====================================
                if data_EventReportArgument['obj'].event_type == philips_constants.NOM_NOTI_MDS_CREAT:
                    data_MDSCreateInfo = self.decoding(philips_struct.MdsCreateInfo, data_EventReportArgument['tail'])
                    ret_dict['MDSCreateInfo'] = dict()
                    ret_dict['MDSCreateInfo']['m_obj_class'] = data_MDSCreateInfo['obj'].m_obj_class
                    ret_dict['MDSCreateInfo']['context_id'] = data_MDSCreateInfo['obj'].context_id
                    ret_dict['MDSCreateInfo']['handle'] = data_MDSCreateInfo['obj'].handle
                    ret_dict['MDSCreateInfo']['count'] = data_MDSCreateInfo['obj'].count
                    ret_dict['MDSCreateInfo']['length'] = data_MDSCreateInfo['obj'].length
                    ret_dict['MDSCreateInfo']['value_list'] = list()

                    tail = data_MDSCreateInfo['tail']

                    for _ in range(data_MDSCreateInfo['obj'].count):
                        #data_AVAType = self.decoding(philips_struct.AVAType, tail)
                        #tail = data_AVAType['tail']

                        data_AVAType = self.decoding(philips_struct.AVAType, tail)
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

                        ret_dict['MDSCreateInfo']['value_list'].append(dict_AVAType_append)


                    #ret_dict['MDSCreateInfo']['handle'] = data_EventReportArgument['obj'].handle


        # = 1. ROLRS_APDU ==========================================================
        elif data_ROapdus['obj'].ro_type == philips_constants.ROLRS_APDU:
            data_ROLRSapdu = self.decoding(philips_struct.ROLRSapdu, data_ROapdus['tail'])

            ret_dict['ROLRSapdu'] = dict()
            ret_dict['ROLRSapdu']['state'] = data_ROLRSapdu['obj'].state
            ret_dict['ROLRSapdu']['count'] = data_ROLRSapdu['obj'].count
            ret_dict['ROLRSapdu']['invoke_id'] = data_ROLRSapdu['obj'].invoke_id
            ret_dict['ROLRSapdu']['command_type'] = data_ROLRSapdu['obj'].command_type
            ret_dict['ROLRSapdu']['length'] = data_ROLRSapdu['obj'].length

        # = 1. ROLRS_APDU ==========================================================
        elif data_ROapdus['obj'].ro_type == philips_constants.ROER_APDU:
            data_ROERapdu = self.decoding(philips_struct.ROERapdu, data_ROapdus['tail'])

            ret_dict['ROERapdu'] = dict()
            ret_dict['ROERapdu']['state'] = data_ROERapdu['obj'].state
            ret_dict['ROERapdu']['count'] = data_ROERapdu['obj'].count
            ret_dict['ROERapdu']['error_value'] = data_ROERapdu['obj'].error_value
            ret_dict['ROERapdu']['length'] = data_ROERapdu['obj'].length


        # = 1. RORS_APDU ===========================================================
        elif data_ROapdus['obj'].ro_type == philips_constants.RORS_APDU:
            data_RORSapdu = self.decoding(philips_struct.RORSapdu, data_ROapdus['tail'])

            ret_dict['RORSapdu'] = dict()
            ret_dict['RORSapdu']['invoke_id'] = data_RORSapdu['obj'].invoke_id
            ret_dict['RORSapdu']['command_type'] = data_RORSapdu['obj'].command_type
            ret_dict['RORSapdu']['length'] = data_RORSapdu['obj'].length

            # = 2. CMD_CONFIRMED_EVENT_REPORT =====================================
            if data_RORSapdu['obj'].command_type == philips_constants.CMD_CONFIRMED_EVENT_REPORT:
                data_EventReportResult = self.decoding(philips_struct.EventReportResult, data_RORSapdu['tail'])

                ret_dict['EventReportResult'] = dict()
                ret_dict['EventReportResult']['m_obj_class'] = data_EventReportResult['obj'].m_obj_class
                ret_dict['EventReportResult']['context_id'] = data_EventReportResult['obj'].context_id
                ret_dict['EventReportResult']['handle'] = data_EventReportResult['obj'].handle
                ret_dict['EventReportResult']['current_time'] = data_EventReportResult['obj'].current_time
                ret_dict['EventReportResult']['event_type'] = data_EventReportResult['obj'].event_type
                ret_dict['EventReportResult']['length'] = data_EventReportResult['obj'].length

            # = 2. CMD_CONFIRMED_ACTION ===========================================
            elif data_RORSapdu['obj'].command_type == philips_constants.CMD_CONFIRMED_ACTION:
                data_ActionResult = self.decoding(philips_struct.ActionResult, data_RORSapdu['tail'])

                ret_dict['ActionResult'] = dict()
                ret_dict['ActionResult']['m_obj_class'] = data_ActionResult['obj'].m_obj_class
                ret_dict['ActionResult']['context_id'] = data_ActionResult['obj'].context_id
                ret_dict['ActionResult']['handle'] = data_ActionResult['obj'].handle
                ret_dict['ActionResult']['action_type'] = data_ActionResult['obj'].action_type
                ret_dict['ActionResult']['length'] = data_ActionResult['obj'].length

                if data_ActionResult['obj'].action_type == philips_constants.NOM_ACT_POLL_MDIB_DATA:
                    data_PollMdibDataReply = self.decoding(philips_struct.PollMdibDataReply, data_ActionResult['tail'])

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

                    data_PollInfoList = self.decoding(philips_struct.PollInfoList, data_PollMdibDataReply['tail'])
                    tail = data_PollInfoList['tail']

                    ret_dict['PollMdibDataReply']['poll_info_list']['count'] = data_PollInfoList['obj'].count
                    ret_dict['PollMdibDataReply']['poll_info_list']['length'] = data_PollInfoList['obj'].length
                    ret_dict['PollMdibDataReply']['poll_info_list']['value'] = list(philips_constants.SingleContextPoll)[
                        data_PollInfoList['obj'].count]

                    # ("value", list(SingleContextPoll)),

                    for _ in range(data_PollInfoList['obj'].count):

                        data_SingleContextPoll = self.decoding(philips_struct.SingleContextPoll, tail)
                        tail = data_SingleContextPoll['tail']

                        # ("value", list(ObservationPoll)),

                        for _ in range(data_SingleContextPoll['obj'].count):
                            data_ObservationPoll = self.decoding(philips_struct.ObservationPoll, tail)
                            tail = data_ObservationPoll['tail']
                            # ("value", list(AVAType)),

                            for _ in range(data_ObservationPoll['obj'].count):
                                data_AVAType = self.decoding(philips_struct.AVAType, tail)
                                tail = data_AVAType['tail']
                                data = tail[0: data_AVAType['obj'].length]
                                # print(f"| data_AVAType.attribute_val   : {data_AVAType['obj'].attribute_val}")
                                #self.file_log_1.write(f"| Data: [{len(data)}] - {data}\n")

                                self.decode_func(data_AVAType['obj'].attribute_id, data_AVAType['obj'].length, data)

                                tail = tail[data_AVAType['obj'].length:len(tail)]




                elif data_ActionResult['obj'].action_type == philips_constants.NOM_ACT_POLL_MDIB_DATA_EXT:
                    data_PollMdibDataReplyExt = self.decoding(philips_struct.PollMdibDataReplyExt,
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

                    data_PollInfoList = self.decoding(philips_struct.PollInfoList, data_PollMdibDataReplyExt['tail'])
                    tail = data_PollInfoList['tail']

                    ret_dict['PollMdibDataReplyExt']['poll_info_list']['count'] = data_PollInfoList['obj'].count
                    ret_dict['PollMdibDataReplyExt']['poll_info_list']['length'] = data_PollInfoList['obj'].length
                    ret_dict['PollMdibDataReplyExt']['poll_info_list']['value_list'] = list()

                    for _ in range(data_PollInfoList['obj'].count):

                        data_SingleContextPoll = self.decoding(philips_struct.SingleContextPoll, tail)
                        tail = data_SingleContextPoll['tail']

                        dict_SingleContextPoll_append = dict()

                        dict_SingleContextPoll_append['context_id'] = data_SingleContextPoll['obj'].context_id
                        dict_SingleContextPoll_append['count'] = data_SingleContextPoll['obj'].count
                        dict_SingleContextPoll_append['length'] = data_SingleContextPoll['obj'].length
                        dict_SingleContextPoll_append['value_list'] = list()

                        for _ in range(data_SingleContextPoll['obj'].count):
                            data_ObservationPoll = self.decoding(philips_struct.ObservationPoll, tail)
                            tail = data_ObservationPoll['tail']

                            dict_ObservationPoll_append = dict()
                            dict_ObservationPoll_append['obj_handle'] = data_ObservationPoll['obj'].obj_handle
                            dict_ObservationPoll_append['count'] = data_ObservationPoll['obj'].count
                            dict_ObservationPoll_append['length'] = data_ObservationPoll['obj'].length
                            dict_ObservationPoll_append['value_list'] = list()

                            for _ in range(data_ObservationPoll['obj'].count):
                                data_AVAType = self.decoding(philips_struct.AVAType, tail)
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
            elif data_RORSapdu['obj'].command_type == philips_constants.CMD_GET:
                data_GetResult = self.decoding(philips_struct.GetResult, data_RORSapdu['tail'])

                ret_dict['GetResult'] = dict()
                ret_dict['GetResult']['m_obj_class'] = data_GetResult['obj'].m_obj_class
                ret_dict['GetResult']['context_id'] = data_GetResult['obj'].context_id
                ret_dict['GetResult']['handle'] = data_GetResult['obj'].handle
                # ret_dict['GetResult']['attributeList'] = data_GetResult['obj'].attributeList

            # = 2. CMD_CONFIRMED_SET =============================================
            elif data_RORSapdu['obj'].command_type == philips_constants.CMD_CONFIRMED_SET:
                data_SetResult = self.decoding(philips_struct.SetResult, data_RORSapdu['tail'])

                ret_dict['SetResult'] = dict()
                ret_dict['SetResult']['m_obj_class'] = data_SetResult['obj'].m_obj_class
                ret_dict['SetResult']['context_id'] = data_SetResult['obj'].context_id
                ret_dict['SetResult']['handle'] = data_SetResult['obj'].handle
                ret_dict['SetResult']['count'] = data_SetResult['obj'].count
                ret_dict['SetResult']['length'] = data_SetResult['obj'].length
                ret_dict['SetResult']['length_tail'] = len(data_RORSapdu['tail'])
                ret_dict['SetResult']['data_list'] = list()
                # ret_dict['SetResult']['attributeList'] = data_SetResult['obj'].attributeList

                tail = data_SetResult['tail']

                for _ in range(data_SetResult['obj'].count):
                    #data_SingleContextPoll = self.decoding(philips_struct.AVAType, tail)
                    #tail = data_SingleContextPoll['tail']

                    #ret_dict['SetResult'] = dict()

                    data_AVAType = self.decoding(philips_struct.AVAType, tail)
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

                    ret_dict['SetResult']['data_list'].append(dict_AVAType_append)

        return ret_dict

    def decode_attribute(self, attribute_id, length, data_array):
        ret_dict = dict()

        if attribute_id == philips_constants.NOM_ATTR_SA_VAL_OBS:

            data_obj = self.decoding(philips_struct.SaObsValue, data_array)
            ret_dict['Attribute'] = 'NOM_ATTR_SA_VAL_OBS'
            ret_dict['physio_id'] = data_obj['obj'].physio_id
            ret_dict['state'] = data_obj['obj'].state
            ret_dict['length'] = data_obj['obj'].length
            ret_dict['data_list'] = self.decode_byte_data(data_obj['tail'])

        elif attribute_id == philips_constants.NOM_ATTR_NU_VAL_OBS:
            data_obj = self.decoding(philips_struct.NuObsValue, data_array)
            ret_dict['Attribute'] = 'NOM_ATTR_NU_VAL_OBS'

            ret_dict['physio_id'] = data_obj['obj'].physio_id
            ret_dict['state'] = data_obj['obj'].state
            ret_dict['unit_code'] = data_obj['obj'].unit_code
            ret_dict['value'] = data_obj['obj'].value

        elif attribute_id == philips_constants.NOM_ATTR_TIME_STAMP_ABS:
            data_obj = self.decoding(philips_struct.AbsoluteTime, data_array)
            ret_dict['Attribute'] = 'NOM_ATTR_TIME_STAMP_ABS'

            ret_dict['century'] = data_obj['obj'].century
            ret_dict['year'] = data_obj['obj'].year
            ret_dict['month'] = data_obj['obj'].month
            ret_dict['day'] = data_obj['obj'].day
            ret_dict['hour'] = data_obj['obj'].hour
            ret_dict['minute'] = data_obj['obj'].minute
            ret_dict['second'] = data_obj['obj'].second
            ret_dict['sec_fractions'] = data_obj['obj'].sec_fractions

        elif attribute_id == philips_constants.NOM_ATTR_NU_CMPD_VAL_OBS:
            data_obj = self.decoding(philips_struct.NuObsValueCmp, data_array)
            ret_dict['Attribute'] = 'NOM_ATTR_NU_CMPD_VAL_OBS'

            ret_dict['count'] = data_obj['obj'].count
            ret_dict['length'] = data_obj['obj'].length
            ret_dict['data_list'] = list()
            # print(data_obj['tail'])

            tail = data_obj['tail']

            for _ in range(data_obj['obj'].count):
                dict_res = dict()
                data_obj = self.decoding(philips_struct.NuObsValue, tail)
                dict_res['physio_id'] = data_obj['obj'].physio_id
                dict_res['state'] = data_obj['obj'].state
                dict_res['unit_code'] = data_obj['obj'].unit_code
                dict_res['value'] = data_obj['obj'].value
                ret_dict['data_list'].append(dict_res)


        elif attribute_id == philips_constants.NOM_ATTR_TIME_STAMP_REL:
            data_obj = self.decoding(philips_struct.RelativeTime, data_array)
            ret_dict['Attribute'] = 'NOM_ATTR_TIME_STAMP_REL'

            ret_dict['RelativeTime'] = data_obj['obj'].RelativeTime

        elif attribute_id == philips_constants.NOM_ATTR_SYS_ID:
            data_obj = self.decoding(philips_struct.VariableLabel, data_array)
            ret_dict['Attribute'] = 'NOM_ATTR_SYS_ID'
            ret_dict['length'] = data_obj['obj'].length

            length = data_obj['obj'].length
            data = data_obj['tail'][0: length]

            ret_dict['SystemID'] = f'{data[0]}.{data[1]}.{data[2]}.{data[3]}.{data[4]}.{data[5]}'


        elif attribute_id == philips_constants.NOM_ATTR_SYS_TYPE:
            data_obj = self.decoding(philips_struct.TYPE, data_array)
            ret_dict['Attribute'] = 'NOM_ATTR_SYS_TYPE'

            ret_dict['partition'] = data_obj['obj'].partition
            ret_dict['code'] = data_obj['obj'].code

        elif attribute_id == philips_constants.NOM_ATTR_ID_ASSOC_NO:
            data_obj = self.decoding(philips_struct.U16, data_array)
            ret_dict['Attribute'] = 'NOM_ATTR_ID_ASSOC_NO'

            ret_dict['InvokeID'] = data_obj['obj'].data

        elif attribute_id == philips_constants.NOM_ATTR_ID_MODEL:
            data_obj = self.decoding(philips_struct.U16, data_array)
            ret_dict['Attribute'] = 'NOM_ATTR_ID_MODEL'

            """
            The manufacturer field is of variable length, hence the offset of model_number depends on the length of
            manufacturer. Currently, the monitor uses 4 characters for the manufacturer and 6 characters for the
            model_number (including the terminating ’\0’).
            """

            str_data = bytearray()

            length = data_obj['obj'].data
            data = data_obj['tail'][0: length]
            tail = data_obj['tail'][length: len(data_obj['tail'])]
            ret_dict['length1'] = length

            index = 0
            for _ in range(length):
                str_data.append(data[index])
                index += 1

            ret_dict['manufacturer'] = str_data.decode('utf-8')

            str_data = bytearray()
            data_obj = self.decoding(philips_struct.U16, tail)
            length = data_obj['obj'].data
            data = data_obj['tail'][0: length]
            ret_dict['length2'] = length

            index = 0
            for _ in range(length):
                str_data.append(data[index])
                index += 1

            ret_dict['model_number'] = str_data.decode('utf-8')


        elif attribute_id == philips_constants.NOM_ATTR_NOM_VERS:
            data_obj = self.decoding(philips_struct.U32, data_array)
            ret_dict['Attribute'] = 'NOM_ATTR_NOM_VERS'
            ret_dict['NomenclatureVersion'] = data_obj['obj'].data

        elif attribute_id == philips_constants.NOM_ATTR_LOCALIZN:
            data_obj = self.decoding(philips_struct.SystemLocal, data_array)
            ret_dict['Attribute'] = 'NOM_ATTR_LOCALIZN'

            ret_dict['text_catalog_revision'] = data_obj['obj'].text_catalog_revision
            ret_dict['language'] = data_obj['obj'].language
            ret_dict['format'] = data_obj['obj'].format


        elif attribute_id == philips_constants.NOM_ATTR_MODE_OP:
            data_obj = self.decoding(philips_struct.U16, data_array)
            ret_dict['Attribute'] = 'NOM_ATTR_MODE_OP'

            # define OPMODE_UNSPEC 0x8000
            # define MONITORING 0x4000
            # define DEMO 0x2000
            # define SERVICE 0x1000
            # define OPMODE_STANDBY 0x0002
            # define CONFIG 0x0001
            ret_dict['OperatingMode'] = data_obj['obj'].data


        elif attribute_id == philips_constants.NOM_ATTR_AREA_APPL:
            data_obj = self.decoding(philips_struct.U16, data_array)
            ret_dict['Attribute'] = 'NOM_ATTR_AREA_APPL'

            # define AREA_UNSPEC 0
            # define AREA_OPERATING_ROOM 1
            # define AREA_INTENSIVE_CARE 2
            # define AREA_NEONATAL_INTENSIVE_CARE 3
            # define AREA_CARDIOLOGY_CARE 4
            ret_dict['ApplicationArea'] = data_obj['obj'].data


        elif attribute_id == philips_constants.NOM_ATTR_LINE_FREQ:
            data_obj = self.decoding(philips_struct.U16, data_array)
            ret_dict['Attribute'] = 'NOM_ATTR_LINE_FREQ'

            # define LINE_F_UNSPEC 0
            # define LINE_F_50HZ 1
            # define LINE_F_60HZ 2
            ret_dict['LineFrequency'] = data_obj['obj'].data

        elif attribute_id == philips_constants.NOM_ATTR_ALTITUDE:
            data_obj = self.decoding(philips_struct.I16, data_array)
            ret_dict['Attribute'] = 'NOM_ATTR_ALTITUDE'

            ret_dict['Altitude'] = data_obj['obj'].data

        elif attribute_id == philips_constants.NOM_ATTR_MDS_GEN_INFO:
            data_obj = self.decoding(philips_struct.MdsGenSystemInfo, data_array)
            ret_dict['Attribute'] = 'NOM_ATTR_MDS_GEN_INFO'

            ret_dict['count'] = data_obj['obj'].count
            ret_dict['length'] = data_obj['obj'].length
            tail = data_obj['tail']

            #for _ in range(data_obj['obj'].count):
            #    data_obj = self.decoding(philips_struct.MdsGenSystemInfoEntry, data_array)
            #    data = data_obj['tail'][0: ]
            #    pass
            # MdsGenSystemInfo

        elif attribute_id == philips_constants.NOM_ATTR_VMS_MDS_STAT:
            data_obj = self.decoding(philips_struct.I16, data_array)
            ret_dict['Attribute'] = 'NOM_ATTR_VMS_MDS_STAT'

            # define DISCONNECTED 0
            # define UNASSOCIATED 1
            # define OPERATING 6
            ret_dict['MDSStatus'] = data_obj['obj'].data

        elif attribute_id == philips_constants.NOM_ATTR_ID_BED_LABEL:
            data_obj = self.decoding(philips_struct.I16, data_array)
            ret_dict['Attribute'] = 'NOM_ATTR_ID_BED_LABEL'

            '''
                String
                The Bed Label can be entered in the Admit/Discharge dialog. It uses 16 bit unicode character
                encoding. Currently, the Bed Label is 17 characters (including terminating ’\0’). If the actual label is
                shorter, the string is filled with ’\0’ characters.
            '''
            ret_dict['LEN'] = len(data_obj['tail'])
            #ret_dict['data'] = data_obj['tail']
            ret_dict['BedLabel'] = data_obj['tail'].decode('utf-8')
            #bytearray_temp = str_data.decode('utf-8')




        elif attribute_id == philips_constants.NOM_ATTR_TIME_ABS:
            data_obj = self.decoding(philips_struct.AbsoluteTime, data_array)
            ret_dict['Attribute'] = 'NOM_ATTR_TIME_ABS'

            ret_dict['century'] = data_obj['obj'].century
            ret_dict['year'] = data_obj['obj'].year
            ret_dict['month'] = data_obj['obj'].month
            ret_dict['day'] = data_obj['obj'].day
            ret_dict['hour'] = data_obj['obj'].hour
            ret_dict['minute'] = data_obj['obj'].minute
            ret_dict['second'] = data_obj['obj'].second
            ret_dict['sec_fractions'] = data_obj['obj'].sec_fractions

        elif attribute_id == philips_constants.NOM_ATTR_TIME_REL:
            data_obj = self.decoding(philips_struct.RelativeTime, data_array)
            ret_dict['Attribute'] = 'NOM_ATTR_TIME_REL'

            ret_dict['RelativeTime'] = data_obj['obj'].RelativeTime


        elif attribute_id == philips_constants.NOM_ATTR_SYS_SPECN:
            data_obj = self.decoding(philips_struct.SystemSpec, data_array)
            ret_dict['Attribute'] = 'NOM_ATTR_SYS_SPECN'
            ret_dict['count'] = data_obj['obj'].count
            ret_dict['length'] = data_obj['obj'].length



            #ret_dict['RelativeTime'] = data_obj['obj'].RelativeTime
            # SystemSpec

        return ret_dict




"""

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

"""



