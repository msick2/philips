import ctypes

import m700_struct
import m700_func
import rcv_data_restore
import data_computer
import data_monitor


class Parser:
    # =======================================================================================================================
    def decoding(self, base_class, array_data):
        obj = base_class.from_buffer(array_data)
        dict_ret = dict()
        dict_ret['obj'] = obj
        dict_ret['tail'] = array_data[ctypes.sizeof(obj):len(array_data)]
        #dict_ret['orn'] = array_data
        return dict_ret

    def extract_u8(self, dict_data):

        ext_data = dict_data['tail'][0]

        dict_data['data'] = ext_data
        dict_data['tail'] = dict_data['tail'][1:len(dict_data)]
        return dict_data

    def extract_u16(self, dict_data):

        ext_data = dict_data['tail'][0] * 256 + dict_data['tail'][1]

        dict_data['data'] = ext_data
        dict_data['tail'] = dict_data['tail'][2:len(dict_data)]
        return dict_data

    def extract_u32(self, dict_data):

        ext_data = dict_data['tail'][3] * 0xffffff + dict_data['tail'][2] * 0xffff + dict_data['tail'][1] * 0xff + dict_data['tail'][0]

        dict_data['data'] = ext_data
        dict_data['tail'] = dict_data['tail'][4:len(dict_data)]
        return dict_data


    # =======================================================================================================================
    def input_data(self, byte_array_data):
        dict_data = m700_func.base_decode(byte_array_data)

        print(f"+============================")
        print(f"| FrameHdr.protocol_id  : {dict_data['obj'].FrameHdr.protocol_id}")
        print(f"| FrameHdr.msg_type     : {dict_data['obj'].FrameHdr.msg_type}")
        print(f"| FrameHdr.length       : {dict_data['obj'].FrameHdr.length}")

        print(f"| SPpdu.session_id      : 0x{dict_data['obj'].SPpdu.session_id:X}")
        print(f"| SPpdu.p_context_id    : {dict_data['obj'].SPpdu.p_context_id}")

        print(f"| ROapdus.ro_type       : {dict_data['obj'].ROapdus.ro_type}")
        print(f"| ROapdus.length        : {dict_data['obj'].ROapdus.length}")

        if dict_data['obj'].ROapdus.ro_type == m700_struct.ROIV_APDU:
            self.ROIVapdu(byte_array_data)

        elif dict_data['obj'].ROapdus.ro_type == m700_struct.RORS_APDU:
            self.RORSapdu(byte_array_data)

        elif dict_data['obj'].ROapdus.ro_type == m700_struct.ROER_APDU:
            self.ROLRSapdu(byte_array_data)

        elif dict_data['obj'].ROapdus.ro_type == m700_struct.ROLRS_APDU:
            self.ROERapdu(byte_array_data)

    # =======================================================================================================================
    def ROIVapdu(self, byte_array_data):  # ROIV_APDU = 1
        dict_data = self.decoding(m700_struct.BaseROIVapdu, byte_array_data)

    # =======================================================================================================================

    def RORSapdu(self, byte_array_data):  # RORS_APDU = 2
        dict_data = self.decoding(m700_struct.BaseRORSapdu, byte_array_data)

        print(f"| RORSapdu.invoke_id    : {dict_data['obj'].RORSapdu.invoke_id}")
        print(f"| RORSapdu.command_type : {dict_data['obj'].RORSapdu.command_type}")
        print(f"| RORSapdu.length       : {dict_data['obj'].RORSapdu.length}")

        if dict_data['obj'].RORSapdu.command_type == m700_struct.CMD_EVENT_REPORT:  # 0
            self.RORSapdu_CMD_EVENT_REPORT(byte_array_data)

        elif dict_data['obj'].RORSapdu.command_type == m700_struct.CMD_CONFIRMED_EVENT_REPORT:  # 1
            self.RORSapdu_CMD_CONFIRMED_EVENT_REPORT(byte_array_data)

        elif dict_data['obj'].RORSapdu.command_type == m700_struct.CMD_GET:  # 3
            self.RORSapdu_CMD_GET(byte_array_data)

        elif dict_data['obj'].RORSapdu.command_type == m700_struct.CMD_SET:  # 4
            self.RORSapdu_CMD_SET(byte_array_data)

        elif dict_data['obj'].RORSapdu.command_type == m700_struct.CMD_CONFIRMED_SET:  # 5
            self.RORSapdu_CMD_CONFIRMED_SET(byte_array_data)

        elif dict_data['obj'].RORSapdu.command_type == m700_struct.CMD_CONFIRMED_ACTION:  # 7
            self.RORSapdu_CMD_CONFIRMED_ACTION(byte_array_data)

    # -----------------------------------------------------------

    def RORSapdu_CMD_EVENT_REPORT(self, byte_array_data):  # 0
        # print("--------------------------------------------------------")
        pass

    def RORSapdu_CMD_CONFIRMED_EVENT_REPORT(self, byte_array_data):  # 1
        # print("--------------------------------------------------------")

        pass

    def RORSapdu_CMD_GET(self, byte_array_data):  # 3
        # print("--------------------------------------------------------")
        pass

    def RORSapdu_CMD_SET(self, byte_array_data):  # 4
        # print("--------------------------------------------------------")
        pass

    def RORSapdu_CMD_CONFIRMED_SET(self, byte_array_data):  # 5
        # print("--------------------------------------------------------")

        pass

    def RORSapdu_CMD_CONFIRMED_ACTION(self, byte_array_data):  # 7
        # print("--------------------------------------------------------")
        dict_data = self.decoding(m700_struct.BaseRORSapdu_ActionResult, byte_array_data)
        print(f"| ActionResult.managed_object.m_obj_class           : {dict_data['obj'].ActionResult.managed_object.m_obj_class}")
        print(f"| ActionResult.managed_object.m_obj_inst.context_id : {dict_data['obj'].ActionResult.managed_object.m_obj_inst.context_id}")
        print(f"| ActionResult.managed_object.m_obj_inst.handle     : {dict_data['obj'].ActionResult.managed_object.m_obj_inst.handle}")
        print(f"| ActionResult.action_type.OIDType                  : {dict_data['obj'].ActionResult.action_type.OIDType}")
        print(f"| ActionResult.length                               : {dict_data['obj'].ActionResult.length}")

        if dict_data['obj'].ActionResult.action_type.OIDType == m700_struct.NOM_ACT_POLL_MDIB_DATA_EXT:
            self.RORSapdu_CMD_CONFIRMED_ACTION_NOM_ACT_POLL_MDIB_DATA_EXT(byte_array_data)

        elif dict_data['obj'].ActionResult.action_type.OIDType == m700_struct.NOM_ACT_POLL_MDIB_DATA:
            self.RORSapdu_CMD_CONFIRMED_ACTION_NOM_ACT_POLL_MDIB_DATA(byte_array_data)

    def RORSapdu_CMD_CONFIRMED_ACTION_NOM_ACT_POLL_MDIB_DATA_EXT(self, byte_array_data):  # 7 -> SingleContextPoll[]
        dict_data = self.decoding(m700_struct.BaseRORSapdu_ActionResult_PollMdibDataReplyExt, byte_array_data)

        print(f"| PollMdibDataReplyExt.poll_number           : {dict_data['obj'].PollMdibDataReplyExt.poll_number}")
        print(f"| PollMdibDataReplyExt.sequence_no           : {dict_data['obj'].PollMdibDataReplyExt.sequence_no}")
        print(f"| PollMdibDataReplyExt.polled_obj_type.partition  : {dict_data['obj'].PollMdibDataReplyExt.polled_obj_type.partition.NomPartition}")
        print(f"| PollMdibDataReplyExt.polled_obj_type.code       : {dict_data['obj'].PollMdibDataReplyExt.polled_obj_type.code.OIDType}")
        print(f"| PollMdibDataReplyExt.polled_attr_grp       : {dict_data['obj'].PollMdibDataReplyExt.polled_attr_grp.OIDType}")

        print(f"| PollMdibDataReplyExt.poll_info_list.count  : {dict_data['obj'].PollMdibDataReplyExt.poll_info_list.count}")
        print(f"| PollMdibDataReplyExt.poll_info_list.length : {dict_data['obj'].PollMdibDataReplyExt.poll_info_list.length}")

        print(f"| Tail len : {len(dict_data['tail'])}")
        #print(f"| Tail : {dict_data['tail']}")

        SingleContextPoll_count = dict_data['obj'].PollMdibDataReplyExt.poll_info_list.count

        print(f"| count : {SingleContextPoll_count}")

        for _ in range(SingleContextPoll_count):
            dict_data = self.decoding(m700_struct.SingleContextPoll, dict_data['tail'])

            print(f"| SingleContextPoll.context_id  : {dict_data['obj'].context_id}")
            print(f"| SingleContextPoll.count       : {dict_data['obj'].count}")
            print(f"| SingleContextPoll.length      : {dict_data['obj'].length}")

            ObservationPoll_count = dict_data['obj'].count

            for _ in range(ObservationPoll_count):
                dict_data = self.decoding(m700_struct.ObservationPoll, dict_data['tail'])

                print(f"| ObservationPoll.context_id : {dict_data['obj'].obj_handle}")
                print(f"| ObservationPoll.count      : {dict_data['obj'].count}")
                print(f"| ObservationPoll.length     : {dict_data['obj'].length}")

                AVAType_count = dict_data['obj'].count

                for _ in range(AVAType_count):
                    dict_data = self.decoding(m700_struct.AVAType, dict_data['tail'])

                    print(f"+-------------------------------------------------------------")
                    print(f"| ObservationPoll.attribute_id  : {dict_data['obj'].attribute_id}")
                    print(f"| ObservationPoll.length        : {dict_data['obj'].length}")
                    print(f"| ObservationPoll.attribute_val : {dict_data['obj'].attribute_val}")




        '''
            typedef struct {
                    u_16                count;
                    u_16                length;
                    SingleContextPoll   value[1];
                } PollInfoList;
    
                typedef struct {
                    u_16            context_id;
                    u_16            count;
                    u_16            length;
                    ObservationPoll value[1];
                } SingleContextPoll;
                
                typedef struct {
                    u_16        obj_handle;
                    u_16        count;
                    u_16        length;
                    AVAType     value[1];
                } ObservationPoll;
            
                typedef struct {
                    u_16 attribute_id;
                    u_16 length;
                    u_16 attribute_val;
                } AVAType;
        '''

        #self.decode_SingleContextPoll(dict_data['tail'])



    def decode_SingleContextPoll(self, byte_array_data):
        dict_data = self.decoding(m700_struct.SingleContextPoll, byte_array_data)

        data_num = dict_data['obj'].context_id
        print(f"| SingleContextPoll.context_id : {dict_data['obj'].context_id.MdsContext}")
        print(f"| SingleContextPoll.poll_info.count : {dict_data['obj'].poll_info.count}")
        print(f"| SingleContextPoll.poll_info.length : {dict_data['obj'].poll_info.length}")


        for _ in range(1):



            pass


        '''
        
            typedef u_16 MdsContext;
        
            typedef struct {
                u_16                count;
                u_16                length;
                SingleContextPoll   value[1];
            } PollInfoList;

            typedef struct {
                u_16            context_id;
                u_16            count;
                u_16            length;
                ObservationPoll value[1];
            } SingleContextPoll;
            
            typedef struct {
                u_16        obj_handle;
                u_16        count;
                u_16        length;
                AVAType     value[1];
            } ObservationPoll;
        
            typedef struct {
                u_16 attribute_id;
                u_16 length;
                u_16 attribute_val;
            } AVAType;
            
            
            
            
            
                typedef struct{
                u_16 count;
                u_16 length;
                AVAType value[1];
            } AttributeList;
                 
             
             
             
             
              
                   typedef struct {
                u_16            context_id;
                poll_info       data
            } SingleContextPoll;       
              
              
              
            struct {
                u_16 count;
                u_16 length;
                ObservationPoll value[1];
            } poll_info;         
                  
        
        '''















    def RORSapdu_CMD_CONFIRMED_ACTION_NOM_ACT_POLL_MDIB_DATA(self, byte_array_data):  # 7
        dict_data = self.decoding(m700_struct.BaseRORSapdu_ActionResult, byte_array_data)

        pass

    # =======================================================================================================================
    def ROLRSapdu(self, byte_array_data):  # ROER_APDU = 3
        dict_data = self.decoding(m700_struct.BaseROLRSapdu, byte_array_data)

    # =======================================================================================================================
    def ROERapdu(self, byte_array_data):  # ROLRS_APDU = 5
        dict_data = self.decoding(m700_struct.BaseROERapdu, byte_array_data)


# =======================================================================================================================


cParser = Parser()

ok = 0
nok = 1

for data in data_monitor.datas4:
    # for data in data_computer.datas1:

    res = rcv_data_restore.input_rcv_data(data)

    if res[0]:
        ok += 1

        cParser.input_data(res[1])

        '''
        <SPpdu>
        <ROapdus>
            ro_type := RORS_APDU
        <RORSapdu>
            invoke_id := "mirrored from event report"
            command_type := CMD_CONFIRMED_EVENT_REPORT 1
        <EventReportResult>
            managed_object := mirrored from event report
            event_type := NOM_NOTI_MDS_CREAT
            length := 0
        '''


    else:
        # print(res[1])
        nok += 1

print("+----------------------------")
print(f"| ok:{ok}, nok:{nok}, {ok * 100 / (ok + nok):3.5}%")
print("+----------------------------")
