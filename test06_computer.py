import ctypes

import m700_struct
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

    # ==================================================================================================================

    def input_data(self, data_bytearray):
        ret_dict = dict()
        print(data_bytearray)
        data_AssocReqSessionHeader = self.decoding(m700_struct.AssocReqSessionHeader, data_bytearray)

        ret_dict['AssocReqSessionHeader'] = dict()
        ret_dict['AssocReqSessionHeader']['SessionHead'] = data_AssocReqSessionHeader['obj'].SessionHead
        ret_dict['AssocReqSessionHeader']['length'] = data_AssocReqSessionHeader['obj'].length


        if(ret_dict['AssocReqSessionHeader']['SessionHead'] == m700_struct.CN_SPDU_SI):
            pass
        elif(ret_dict['AssocReqSessionHeader']['SessionHead'] == m700_struct.AC_SPDU_SI):
            pass
        elif (ret_dict['AssocReqSessionHeader']['SessionHead'] == m700_struct.RF_SPDU_SI):
            pass
        elif (ret_dict['AssocReqSessionHeader']['SessionHead'] == m700_struct.FN_SPDU_SI):
            pass
        elif (ret_dict['AssocReqSessionHeader']['SessionHead'] == m700_struct.DN_SPDU_SI):
            pass
        elif (ret_dict['AssocReqSessionHeader']['SessionHead'] == m700_struct.AB_SPDU_SI):
            pass




        return ret_dict







cParser = Parser()

ok = 0
nok = 1

index = 0

# res = rcv_data_restore.input_rcv_data(data_monitor.datas4[4997])
# cParser.get_data(res[1])

file_print = open("file_print_C1.txt", "w")

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

print(f"OK: {ok}, OK:{nok} {((ok - nok) / ok) * 100}%")

file_print.close()






