"""
일단은....
전송을 하는 패킷을 만든다.
1. 원하는 데이터가 나올 수 있도록 해야 한다.
2. 주기적으로 날려야 한다.
3. 날리는 모양이 몇가지 패턴이 있는게 그게 뭘까?
4. 받는것의 응답이 있는건지 뭐 그런걸 알아야 한다.
5. 모아놓은것을 기반으로 그것과 같은 문자열이 나올때 까지 만들면 될듯 함.

"""

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

    def input_data(self, data_bytearray):
        ret_dict = dict()
        data_FrameHdr = self.decoding(philips_struct.FrameHdr, data_bytearray)
        data_AssocReqSessionHeader = self.decoding(philips_struct.AssocReqSessionHeader, data_FrameHdr['tail'])
        data_AssocReqSessionData = self.decoding(philips_struct.AssocReqSessionData, data_AssocReqSessionHeader['tail'])

        # data_SPpdu = self.decoding(philips_struct.SPpdu, data_FrameHdr['tail'])
        # data_ROapdus = self.decoding(philips_struct.ROapdus, data_SPpdu['tail'])



        ret_dict['FrameHdr'] = dict()
        ret_dict['FrameHdr']['protocol_id'] = data_FrameHdr['obj'].protocol_id
        ret_dict['FrameHdr']['msg_type'] = data_FrameHdr['obj'].msg_type
        ret_dict['FrameHdr']['length'] = data_FrameHdr['obj'].length

        ret_dict['AssocReqSessionHeader'] = dict()
        ret_dict['AssocReqSessionHeader']['SessionHead'] = data_AssocReqSessionHeader['obj'].SessionHead
        ret_dict['AssocReqSessionHeader']['length'] = data_AssocReqSessionHeader['obj'].length

        ret_dict['AssocReqSessionData'] = dict()
        ret_dict['AssocReqSessionData']['d00'] = data_AssocReqSessionData['obj'].d00
        ret_dict['AssocReqSessionData']['d01'] = data_AssocReqSessionData['obj'].d01
        ret_dict['AssocReqSessionData']['d02'] = data_AssocReqSessionData['obj'].d02
        ret_dict['AssocReqSessionData']['d03'] = data_AssocReqSessionData['obj'].d03
        ret_dict['AssocReqSessionData']['d04'] = data_AssocReqSessionData['obj'].d04
        ret_dict['AssocReqSessionData']['d05'] = data_AssocReqSessionData['obj'].d05
        ret_dict['AssocReqSessionData']['d06'] = data_AssocReqSessionData['obj'].d06
        ret_dict['AssocReqSessionData']['d07'] = data_AssocReqSessionData['obj'].d07
        ret_dict['AssocReqSessionData']['d08'] = data_AssocReqSessionData['obj'].d08
        ret_dict['AssocReqSessionData']['d09'] = data_AssocReqSessionData['obj'].d09
        ret_dict['AssocReqSessionData']['d10'] = data_AssocReqSessionData['obj'].d10
        ret_dict['AssocReqSessionData']['d11'] = data_AssocReqSessionData['obj'].d11
        ret_dict['AssocReqSessionData']['d12'] = data_AssocReqSessionData['obj'].d12
        ret_dict['AssocReqSessionData']['d13'] = data_AssocReqSessionData['obj'].d13


        print(len(data_bytearray))
        print(len(data_FrameHdr['tail']))
        print(len(data_AssocReqSessionHeader['tail']))
        print(len(data_AssocReqSessionData['tail']))



        return ret_dict


cParser = Parser()

ok = 0
nok = 1

index = 0

# res = rcv_data_restore.input_rcv_data(data_monitor.datas4[4997])
# cParser.get_data(res[1])

file_print = open("file_print_trans.json", "w")

for data in data_computer.datas1:
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

    if index == 3:
        break




file_print.close()
