import ctypes
import matplotlib.pyplot as plt

import m700_struct
import rcv_data_restore
import data_computer
import data_monitor



dict_data = dict()


class Parser:

    def __init__(self):
        self.file_log_1 = open("file_log_1.txt", "w")
        self.file_log_2 = open("file_log_2.txt", "w")


    def __del__(self):
        self.file_log_1.close()
        self.file_log_2.close()


    # ==================================================================================================================
    def decoding(self, base_class, byte_array_data):
        obj = base_class.from_buffer(byte_array_data)

        dict_ret = \
            {
                'obj'  : obj,
                'tail' : byte_array_data[ctypes.sizeof(obj):len(byte_array_data)],
            }

        return dict_ret


    # ==================================================================================================================

    def get_data(self, byte_array_data):
        data_FrameHdr   = self.decoding(m700_struct.FrameHdr,   byte_array_data)
        data_SPpdu      = self.decoding(m700_struct.SPpdu,      data_FrameHdr['tail'])
        data_ROapdus    = self.decoding(m700_struct.ROapdus,    data_SPpdu['tail'])

        self.file_log_1.write(f"+ Base FrameHdr ===================\n")
        self.file_log_1.write(f"| FrameHdr.protocol_id  : {data_FrameHdr['obj'].protocol_id}\n")
        self.file_log_1.write(f"| FrameHdr.msg_type     : {data_FrameHdr['obj'].msg_type}\n")
        self.file_log_1.write(f"| FrameHdr.length       : {data_FrameHdr['obj'].length}\n")
        self.file_log_1.write(f"+ Base SPpdu =====================\n")

        self.file_log_1.write(f"| SPpdu.session_id      : 0x{data_SPpdu['obj'].session_id:X}\n")  # contains a fixed value 0xE100
        self.file_log_1.write(f"| SPpdu.p_context_id    : {data_SPpdu['obj'].p_context_id}\n")    # negotiated in association phase

        self.file_log_1.write(f"+ Base ROapdus ===================\n")
        self.file_log_1.write(f"| ROapdus.ro_type       : {data_ROapdus['obj'].ro_type}\n")
        self.file_log_1.write(f"| ROapdus.length        : {data_ROapdus['obj'].length}\n")


        #self.file_log_1.write(f"+ Base FrameHdr ===================\n")
        #self.file_log_1.write(f"| FrameHdr.protocol_id  : {data_FrameHdr['obj'].protocol_id}\n")
        #self.file_log_1.write(f"| FrameHdr.msg_type     : {data_FrameHdr['obj'].msg_type}\n")
        #self.file_log_1.write(f"| FrameHdr.length       : {data_FrameHdr['obj'].length}\n")
        #self.file_log_1.write(f"+ Base SPpdu =====================\n")
        #
        #self.file_log_1.write(f"| SPpdu.session_id      : 0x{data_SPpdu['obj'].session_id:X}\n")  # contains a fixed value 0xE100
        #self.file_log_1.write(f"| SPpdu.p_context_id    : {data_SPpdu['obj'].p_context_id}\n")    # negotiated in association phase
        #
        #self.file_log_1.write(f"+ Base ROapdus ===================\n")
        #self.file_log_1.write(f"| ROapdus.ro_type       : {data_ROapdus['obj'].ro_type}\n")
        #self.file_log_1.write(f"| ROapdus.length        : {data_ROapdus['obj'].length}\n")

        if data_ROapdus['obj'].ro_type == m700_struct.ROIV_APDU:
            self.file_log_1.write(f"+ LV 1 ROIVapdu ==============\n")
            self.ROIVapdu(data_ROapdus)

        elif data_ROapdus['obj'].ro_type == m700_struct.RORS_APDU:
            self.file_log_1.write(f"+ LV 1 ROIVapdu ==============\n")
            self.RORSapdu(data_ROapdus)

        elif data_ROapdus['obj'].ro_type == m700_struct.ROER_APDU:
            self.file_log_1.write(f"+ LV 1 ROIVapdu ==============\n")
            self.ROERapdu(data_ROapdus)

        elif data_ROapdus['obj'].ro_type == m700_struct.ROLRS_APDU:
            self.file_log_1.write(f"+ LV 1 ROIVapdu ==============\n")
            self.ROLRSapdu(data_ROapdus)

    # ------------------------------------------------------------------------------------------------------------------
    def ROIVapdu(self, data_ROapdus):
        data_ROIVapdu = self.decoding(m700_struct.ROIVapdu, data_ROapdus['tail'])

    def RORSapdu(self, data_ROapdus):

        data_RORSapdu = self.decoding(m700_struct.RORSapdu, data_ROapdus['tail'])

        self.file_log_1.write(f"| RORSapdu.invoke_id     : {data_RORSapdu['obj'].invoke_id}\n")

        self.file_log_1.write(f"+ CMDType --------------------+---+\n")
        self.file_log_1.write(f"| CMD_EVENT_REPORT            : 0 |\n")
        self.file_log_1.write(f"| CMD_CONFIRMED_EVENT_REPORT  : 1 |\n")
        self.file_log_1.write(f"| CMD_GET                     : 3 |\n")
        self.file_log_1.write(f"| CMD_SET                     : 4 |\n")
        self.file_log_1.write(f"| CMD_CONFIRMED_SET           : 5 |\n")
        self.file_log_1.write(f"| CMD_CONFIRMED_ACTION        : 7 |\n")
        self.file_log_1.write(f"+-----------------------------+---+\n")

        self.file_log_1.write(f"| RORSapdu.command_type  : {data_RORSapdu['obj'].command_type}\n")  # 구조에 추가 될 명령 데이터 유형을 정의함.
        self.file_log_1.write(f"| RORSapdu.length        : {data_RORSapdu['obj'].length} - {len(data_RORSapdu['tail'])}\n")


        if data_RORSapdu['obj'].command_type == m700_struct.CMD_EVENT_REPORT:
            self.file_log_1.write(f"+ LV 1 ROIVapdu ==============\n")
            self.RORSapdu_CMD_EVENT_REPORT(data_RORSapdu)

        elif data_RORSapdu['obj'].command_type == m700_struct.CMD_CONFIRMED_EVENT_REPORT:
            self.RORSapdu_CMD_CONFIRMED_EVENT_REPORT(data_RORSapdu)

        elif data_RORSapdu['obj'].command_type == m700_struct.CMD_GET:
            self.RORSapdu_CMD_GET(data_RORSapdu)

        elif data_RORSapdu['obj'].command_type == m700_struct.CMD_SET:
            self.RORSapdu_CMD_SET(data_RORSapdu)

        elif data_RORSapdu['obj'].command_type == m700_struct.CMD_CONFIRMED_SET:
            self.RORSapdu_CMD_CONFIRMED_SET(data_RORSapdu)

        elif data_RORSapdu['obj'].command_type == m700_struct.CMD_CONFIRMED_ACTION:
            self.RORSapdu_CMD_CONFIRMED_ACTION(data_RORSapdu)

    def RORSapdu_CMD_EVENT_REPORT(self, data_RORSapdu):
        pass

    def RORSapdu_CMD_CONFIRMED_EVENT_REPORT(self, data_RORSapdu):
        pass

    def RORSapdu_CMD_GET(self, data_RORSapdu):
        pass

    def RORSapdu_CMD_SET(self, data_RORSapdu):
        pass

    def RORSapdu_CMD_CONFIRMED_SET(self, data_RORSapdu):

        pass

    def RORSapdu_CMD_CONFIRMED_ACTION(self, data_RORSapdu):
        self.file_log_1.write(f"+ RORSapdu_CMD_CONFIRMED_ACTION ===========================================\n")
        data_ActionResult = self.decoding(m700_struct.ActionResult, data_RORSapdu['tail'])

        self.file_log_1.write(f"| ActionResult.m_obj_class   : {data_ActionResult['obj'].m_obj_class}\n")
        self.file_log_1.write(f"| ActionResult.context_id    : {data_ActionResult['obj'].context_id}\n")
        self.file_log_1.write(f"| ActionResult.handle        : {data_ActionResult['obj'].handle}\n")
        self.file_log_1.write(f"| ActionResult.action_type   : {data_ActionResult['obj'].action_type}\n")
        self.file_log_1.write(f"| ActionResult.length        : {data_ActionResult['obj'].length} - {len(data_ActionResult['tail'])}\n")

        if data_ActionResult['obj'].action_type == m700_struct.NOM_ACT_POLL_MDIB_DATA_EXT and data_ActionResult['obj'].m_obj_class == m700_struct.NOM_MOC_VMS_MDS:
            self.RORSapdu_CMD_CONFIRMED_ACTION_NOM_ACT_POLL_MDIB_DATA_EXT(data_ActionResult)

        if data_ActionResult['obj'].action_type == m700_struct.NOM_ACT_POLL_MDIB_DATA:
            self.RORSapdu_CMD_CONFIRMED_ACTION_NOM_ACT_POLL_MDIB_DATA(data_ActionResult)

    def RORSapdu_CMD_CONFIRMED_ACTION_NOM_ACT_POLL_MDIB_DATA(self, data_ActionResult):
        self.file_log_1.write(f"+ RORSapdu_CMD_CONFIRMED_ACTION_NOM_ACT_POLL_MDIB_DATA ================\n")

        data_PollMdibDataReq = self.decoding(m700_struct.PollMdibDataReq, data_ActionResult['tail']) ###



    def RORSapdu_CMD_CONFIRMED_ACTION_NOM_ACT_POLL_MDIB_DATA_EXT(self, data_ActionResult):
        self.file_log_1.write(f"+ RORSapdu_CMD_CONFIRMED_ACTION_NOM_ACT_POLL_MDIB_DATA_EXT ================\n")

        data_PollMdibDataReplyExt = self.decoding(m700_struct.PollMdibDataReplyExt, data_ActionResult['tail'])

        self.file_log_1.write(f"| PollMdibDataReplyExt.poll_number      : {data_PollMdibDataReplyExt['obj'].poll_number}\n")
        self.file_log_1.write(f"| PollMdibDataReplyExt.sequence_no      : {data_PollMdibDataReplyExt['obj'].sequence_no}\n")
        self.file_log_1.write(f"| PollMdibDataReplyExt.rel_time_stamp   : {data_PollMdibDataReplyExt['obj'].rel_time_stamp}\n")
        self.file_log_1.write(f"| PollMdibDataReplyExt.century          : {data_PollMdibDataReplyExt['obj'].century}\n")
        self.file_log_1.write(f"| PollMdibDataReplyExt.year             : {data_PollMdibDataReplyExt['obj'].year}\n")
        self.file_log_1.write(f"| PollMdibDataReplyExt.month            : {data_PollMdibDataReplyExt['obj'].month}\n")
        self.file_log_1.write(f"| PollMdibDataReplyExt.day              : {data_PollMdibDataReplyExt['obj'].day}\n")
        self.file_log_1.write(f"| PollMdibDataReplyExt.hour             : {data_PollMdibDataReplyExt['obj'].hour}\n")
        self.file_log_1.write(f"| PollMdibDataReplyExt.minute           : {data_PollMdibDataReplyExt['obj'].minute}\n")
        self.file_log_1.write(f"| PollMdibDataReplyExt.second           : {data_PollMdibDataReplyExt['obj'].second}\n")
        self.file_log_1.write(f"| PollMdibDataReplyExt.sec_fractions    : {data_PollMdibDataReplyExt['obj'].sec_fractions}\n")
        self.file_log_1.write(f"| PollMdibDataReplyExt.partition        : {data_PollMdibDataReplyExt['obj'].partition}\n")
        self.file_log_1.write(f"| PollMdibDataReplyExt.code             : {data_PollMdibDataReplyExt['obj'].code}\n")
        self.file_log_1.write(f"| PollMdibDataReplyExt.polled_attr_grp  : {data_PollMdibDataReplyExt['obj'].polled_attr_grp}\n")

        # print(f"| PollMdibDataReplyExt.count            : {data_PollMdibDataReplyExt['obj'].count}")
        # print(f"| PollMdibDataReplyExt.length           : {data_PollMdibDataReplyExt['obj'].length} - {len(data_PollMdibDataReplyExt['tail'])}")

        self.PollInfoList(data_PollMdibDataReplyExt['tail'])

        #tail = data_PollMdibDataReplyExt['tail']
#
        #for _ in range(data_PollMdibDataReplyExt['obj'].count):
        #    data_SingleContextPoll = self.decoding(m700_struct.SingleContextPoll, tail)
        #    tail = data_SingleContextPoll['tail']
#
        #    print(f"+ SingleContextPoll ===========================")
        #    print(f"| tail length : {len(tail)}")
#
        #    print(f"| SingleContextPoll.context_id      : {data_SingleContextPoll['obj'].context_id}") #
        #    print(f"| SingleContextPoll.count           : {data_SingleContextPoll['obj'].count}")
        #    print(f"| SingleContextPoll.length          : {data_SingleContextPoll['obj'].length}")
#
        #    for _ in range(data_SingleContextPoll['obj'].count):
        #        data_ObservationPoll = self.decoding(m700_struct.ObservationPoll, tail)
        #        tail = data_ObservationPoll['tail']
        #        print(f"+ ObservationPoll ================")
        #        print(f"| tail length : {len(tail)}")
#
        #        print(f"| ObservationPoll.obj_handle     : {data_ObservationPoll['obj'].obj_handle}")   # 객체 인스턴스를 식별함.
        #        print(f"| ObservationPoll.count          : {data_ObservationPoll['obj'].count}")
        #        print(f"| ObservationPoll.length         : {data_ObservationPoll['obj'].length}")
#
        #    print(f"+ =============================================")


    def PollInfoList(self, tail):
        data_PollInfoList = self.decoding(m700_struct.PollInfoList, tail)
        tail = data_PollInfoList['tail']
        self.file_log_1.write(f"+ PollInfoList = [{len(tail)}] ==================================\n")
        self.file_log_1.write(f"| PollInfoList.count            : {data_PollInfoList['obj'].count}\n")
        self.file_log_1.write(f"| PollInfoList.length           : {data_PollInfoList['obj'].length} - {len(data_PollInfoList['tail'])}\n")
        # ("value", list(SingleContextPoll)),

        for _ in range(data_PollInfoList['obj'].count):

            data_SingleContextPoll = self.decoding(m700_struct.SingleContextPoll, tail)
            tail = data_SingleContextPoll['tail']

            self.file_log_1.write(f"+ SingleContextPoll = [{len(tail)}] ==========================\n")
            self.file_log_1.write(f"| SingleContextPoll.context_id      : {data_SingleContextPoll['obj'].context_id}\n") #
            self.file_log_1.write(f"| SingleContextPoll.count           : {data_SingleContextPoll['obj'].count}\n")
            self.file_log_1.write(f"| SingleContextPoll.length          : {data_SingleContextPoll['obj'].length}\n")
            # ("value", list(ObservationPoll)),

            for _ in range(data_SingleContextPoll['obj'].count):
                data_ObservationPoll = self.decoding(m700_struct.ObservationPoll, tail)
                tail = data_ObservationPoll['tail']
                self.file_log_1.write(f"+ ObservationPoll = [{len(tail)}] ==============\n")
                self.file_log_1.write(f"| ObservationPoll.obj_handle     : {data_ObservationPoll['obj'].obj_handle}\n")   # 객체 인스턴스를 식별함.
                self.file_log_1.write(f"| ObservationPoll.count          : {data_ObservationPoll['obj'].count}\n")
                self.file_log_1.write(f"| ObservationPoll.length         : {data_ObservationPoll['obj'].length}\n")
                # ("value", list(AVAType)),

                for _ in range(data_ObservationPoll['obj'].count):
                    data_AVAType = self.decoding(m700_struct.AVAType, tail)
                    tail = data_AVAType['tail']
                    data = tail[0 : data_AVAType['obj'].length]
                    self.file_log_1.write(f"+ AVAType = [{len(tail)}] ========\n")
                    self.file_log_1.write(f"| data_AVAType.attribute_id    : {data_AVAType['obj'].attribute_id}\n")  # 객체 인스턴스를 식별함.
                    self.file_log_1.write(f"| data_AVAType.length          : {data_AVAType['obj'].length}\n")
                    #print(f"| data_AVAType.attribute_val   : {data_AVAType['obj'].attribute_val}")
                    self.file_log_1.write(f"| Data: [{len(data)}] - {data}\n")

                    self.decode_func(data_AVAType['obj'].attribute_id, data_AVAType['obj'].length, data)

                    tail = tail[data_AVAType['obj'].length:len(tail)]


        self.file_log_1.write(f"+ =============================================\n")



    def ROLRSapdu(self, data_ROapdus):
        data_ROLRSapdu = self.decoding(m700_struct.ROLRSapdu, data_ROapdus['tail'])

    def ROERapdu(self, data_ROapdus):
        data_ROERapdu = self.decoding(m700_struct.ROERapdu, data_ROapdus['tail'])


    def decode_func(self, id, len, data_array):
        if id in dict_data:
            # dict_data[data_AVAType['obj'].attribute_id].append(data_AVAType['obj'].attribute_val)
            dict_data[id].append(data_array)
        else:
            dict_data[id] = list()
            dict_data[id].append(data_array)
            # dict_data[data_AVAType['obj'].attribute_id].append(data_AVAType['obj'].attribute_val)


        # if id == m700_struct.NOM_ATTR_TIME_STAMP_ABS:



# ======================================================================================================================


cParser = Parser()

ok = 0
nok = 1

index = 0

#res = rcv_data_restore.input_rcv_data(data_monitor.datas4[4997])
#cParser.get_data(res[1])


for data in data_monitor.datas4:
    # for data in data_computer.datas1:

    res = rcv_data_restore.input_rcv_data(data)

    if res[0]:
        ok += 1

        cParser.get_data(res[1])
        #print(f"* Index: {index}")


    else:
        # print(res[1])
        nok += 1

    index += 1



print("+----------------------------")
print(f"| ok:{ok}, nok:{nok}, {ok * 100 / (ok + nok):3.5}%")
print("+----------------------------")
#print(dict_data)


def decoding_(base_class, byte_array_data):
    obj = base_class.from_buffer(byte_array_data)

    dict_ret = \
        {
            'obj': obj,
            'tail': byte_array_data[ctypes.sizeof(obj):len(byte_array_data)],
        }

    return dict_ret

listdata = list()

save_file_id = open("savefile_id.txt", "w")
save_file_data = open("savefile_data.txt", "w")

dict_piso = dict()

dict_piso[19380] = list()
dict_piso[18964] = list()
dict_piso[258] = list()

for data in dict_data:
    #print (data)
    save_file_id.write(f"{data}, ")
    for array in dict_data[data]:
        #print (array)
        if data == 2448:
            obj_data = decoding_(m700_struct.RelativeTime, array)
            #print(obj_data['obj'].RelativeTime)

        elif data == 62007:
            pass
        elif data == 63896:
            pass
        elif data == 2379:
            pass
        elif data == 2384:
            obj_data = decoding_(m700_struct.NuObsValue, array)
            #print(f"physio_id : {obj_data['obj'].physio_id} ================")
            #print(f"state     : {obj_data['obj'].state}")
            #print(f"unit_code : {obj_data['obj'].unit_code}")
            #print(f"value     : {obj_data['obj'].value}")



        elif data == 2449:
            obj_data = decoding_(m700_struct.RelativeTime, array)
            #print(f"RelativeTime     : {obj_data['obj'].RelativeTime}")
            pass
        elif data == 61448:
            pass
        elif data == 2414:
            obj_data = decoding_(m700_struct.SaObsValue, array)
            #print(f"physio_id  : {obj_data['obj'].physio_id}")
            #print(f"state      : {obj_data['obj'].state}")
            #print(f"length     : {obj_data['obj'].length} - {len(obj_data['tail'])}")

            dict_piso[obj_data['obj'].physio_id].append(obj_data['tail'])

            #front = 0
            #back = 0
            #flag = 0
            #for data_byte in obj_data['tail']:
            #    if flag == 0:
            #        front = data_byte * 256
            #        flag = 1
            #    else:
            #        flag = 0
            #        print(front + data_byte)
            #        save_file_data.write(f"{front + data_byte}\n")

save_file_id.close()
save_file_data.close()

#save_file_id = open("savefile_id.txt", "w")

for list in dict_piso:
    #print(list)
    #print(dict_piso[list])
    save_file_id = open(f"savefile_phy{list}.txt", "w")

    for data in dict_piso[list]:

        #save_file_id.write(f"{byte_data}\n")

        front = 0
        back = 0
        flag_ = 0
        for byte_data in data:
           if flag_ == 0:
               front = byte_data * 256
               flag_ = 1
           else:
               flag_ = 0
               #print(front + byte_data)
               save_file_id.write(f"{front + byte_data}\n")


    save_file_id.close()





'''
NOM_SAT_O2_TONE_FREQ        61448
NOM_ATTR_TIME_STAMP_REL     2449
NOM_ATTR_NU_VAL_OBS         2384
NOM_ATTR_NU_CMPD_VAL_OBS    2379
NOM_ATTR_TIME_STAMP_ABS     2448

'''
