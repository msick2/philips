

import rcv_data_restore
import data_computer
import data_monitor



def get_8bit_int(data):
    return data

def get_16bit_int(data):
    num = data[0] * 256 + data[1]
    return num

def get_32bit_int(data):
    num = data[0] * 0xffffff + data[1] * 0xffff + data[2] * 0xff + data[3]
    return num


def get_common_header(data):
    header = data[0:12]
    #SPpdu = data[4:8]
    #ROapdus = data[8:12]
    data_next = data[12:len(data)]


    procotol_id = get_8bit_int(header[0])
    msg_type = get_8bit_int(header[1])
    data_len = get_16bit_int(header[2:4])

    session_id = get_16bit_int(header[4:6])
    p_context_id = get_16bit_int(header[6:8])

    ro_type = get_16bit_int(header[8:10])
    length = get_16bit_int(header[10:12])


    #procotol_id = header[0]
    #msg_type = header[1]
    #data_len = header[2] * 256 + header[3]
    #session_id = header[4] * 256 + header[5]
    #p_context_id = header[6] * 256 + header[7]
    #ro_type = header[8] * 256 + header[9]
    #length = header[10] * 256 + header[11]


    #print("-------------------")
    #print( "   data orn: " + ''.join('0x{:02x} '.format(x) for x in data))
    #print( "  data next: " + ''.join('0x{:02x} '.format(x) for x in data_next))
    #print( "       data: " + ''.join('0x{:02x} '.format(x) for x in header))
    #print(f"protocol_id: {procotol_id}")
    #print(f"   msg_type: {msg_type}")
    #print(f"   data_len: {data_len:3} - {len(data) - 4:3} -> {len(data) - 4 - data_len}")

    contain = {
        "procotol_id" : procotol_id,
        "msg_type" : msg_type,
        "data_len" : data_len,
        "session_id": session_id,
        "p_context_id": p_context_id,
        "ro_type": ro_type,
        "length": length,
    }

    return (contain , data_next)



def get_RORSapdu(data):
    header = data[0:12]
    data_next = data[12:len(data)]

    invoke_id = get_16bit_int(header[0:2])
    command_type = get_16bit_int(header[2:4])
    length = get_16bit_int(header[4:6])

    contain = {
        "invoke_id" : invoke_id,
        "command_type" : command_type,
        "length" : length,
    }

    return (contain , data_next)

def get_ROIVapdu(data):
    header = data[0:12]
    data_next = data[12:len(data)]

    invoke_id = get_16bit_int(header[0:2])
    command_type = get_16bit_int(header[2:4])
    length = get_16bit_int(header[4:6])

    contain = {
        "invoke_id" : invoke_id,
        "command_type" : command_type,
        "length" : length,
    }

    return (contain , data_next)



'''
typedef struct {
u_8 state;
# define RORLS_FIRST 1 /* set in the first message */
# define RORLS_NOT_FIRST_NOT_LAST 2
# define RORLS_LAST 3 /* last RORLSapdu, one RORSapdu
to follow */
u_8 count; /* counter starts with 1 */
} RorlsId;
'''

def get_ROLRSapdu(data):
    header = data[0:14]
    data_next = data[14:len(data)]

    state = get_8bit_int(header[0])
    count = get_8bit_int(header[1])
    invoke_id = get_16bit_int(header[2:4])
    command_type = get_16bit_int(header[4:6])
    length = get_16bit_int(header[6:8])

    contain = {
        "state" : state,
        "count" : count,
        "invoke_id" : invoke_id,
        "command_type" : command_type,
        "length" : length,
    }

    return (contain , data_next)


def get_PollInfoList(data):
    header = data[0:4]
    data_next = data[4:len(data)]

    count = get_16bit_int(header[0:2])
    length = get_16bit_int(header[2:4])

    contain = {
        "count" : count,
        "length" : length,
    }

    return (contain , data_next)






ok = 0
nok = 1

for data in data_monitor.datas3:
#for data in data_computer.datas3:

    # print(data_computer.data)

    res = rcv_data_restore.input_rcv_data(data)

    if res[0] == True:
        #print(res[1])
        ok += 1
        res_header = get_common_header(res[1])
        #res_SPpdu = get_SPpdu(res[1])

        #print("-------------------")
        #print( "        data: " + ''.join('0x{:02x} '.format(x) for x in res[1]))
        #print( "   data next: " + ''.join('0x{:02x} '.format(x) for x in res_header[1]))
        #print(f" protocol_id: {res_header[0]['procotol_id']}")
        #print(f"    msg_type: {res_header[0]['msg_type']}")
        #print(f"    data_len: {res_header[0]['data_len']} - {len(res_header[1]) + 8}")
        #print(f"  session_id: {res_header[0]['session_id']:x}")
        #print(f"p_context_id: {res_header[0]['p_context_id']}")
        #print(f"     ro_type: {res_header[0]['ro_type']}")
        #print(f"      length: {res_header[0]['length']} - {len(res_header[1])}")

        if res_header[0]['ro_type'] == 1:
            #print("ROIV_APDU")
            res_ROIV = get_ROIVapdu(res_header[1])
            #print(f"   invoke_id: {res_ROIV[0]['invoke_id']:x} command_type: {res_ROIV[0]['command_type']} length: {res_ROIV[0]['length']}")
            pass

        # RORSapdu : 원격 작업 결과 메시지는 확인이 필요한 작업 호출 메시지에 대한 응답입니다.
        elif res_header[0]['ro_type'] == 2:
            #print("RORS_APDU")
            res_RORS = get_RORSapdu(res_header[1])
            #print(f"   invoke_id: {res_RORS[0]['invoke_id']:x} command_type: {res_RORS[0]['command_type']} length: {res_RORS[0]['length']}")
            pass


        elif res_header[0]['ro_type'] == 3:
            #print("ROER_APDU")
            pass

        # ROLRS_APDU
        # state 1: 해당 데이터의 시작
        # state 3: 해당 데이터의 마지막
        # count : 해당 데이터 조각의 순번

        elif res_header[0]['ro_type'] == 5:
            #print("ROLRS_APDU")

            print("-------------------")
            print( "        data: " + ''.join('0x{:02x} '.format(x) for x in res[1]))
            print( "   data next: " + ''.join('0x{:02x} '.format(x) for x in res_header[1]))
            print(f" protocol_id: {res_header[0]['procotol_id']}")
            print(f"    msg_type: {res_header[0]['msg_type']}")
            print(f"    data_len: {res_header[0]['data_len']} - {len(res_header[1]) + 8}")
            print(f"  session_id: {res_header[0]['session_id']:x}")
            print(f"p_context_id: {res_header[0]['p_context_id']}")
            print(f"     ro_type: {res_header[0]['ro_type']}")
            print(f"      length: {res_header[0]['length']} - {len(res_header[1])}")

            res_RORS = get_ROLRSapdu(res_header[1])
            print(f" state:{res_RORS[0]['state']:x}  count:{res_RORS[0]['count']:x} invoke_id: {res_RORS[0]['invoke_id']:x} command_type: {res_RORS[0]['command_type']} length: {res_RORS[0]['length']}")
            print("res_RORS: " + ''.join('0x{:02x} '.format(x) for x in res_RORS[1]))

            res_PollInfoList = get_PollInfoList(res_RORS[1])
            print(f" count:{res_RORS[0]['count']:x} length: {res_RORS[0]['length']}")
            print("res_PollInfoList: " + ''.join('0x{:02x} '.format(x) for x in res_PollInfoList[1]))


            pass

        else:
            print(f"{res_header[0]['ro_type']}*******************************")

    else:
        #print(res[1])
        nok += 1

print("-------------------")
print(f"ok:{ok}, nok:{nok}, {ok * 100 / (ok + nok)}%")


"""
#define CMD_EVENT_REPORT 0
#define CMD_CONFIRMED_EVENT_REPORT 1
#define CMD_GET 3
#define CMD_SET 4
#define CMD_CONFIRMED_SET 5
#define CMD_CONFIRMED_ACTION 7

"""



"""
SPpdu 
    session_id : 0xE100
    p_context_id : 2
        {0xE1 0x00 0x00 0x02}
ROapdus 
    ro_type : RORS_APDU
    length : 20
        {0x00 0x02 0x00 0x14}
RORSapdu 
    invoke_id : 1
    command_type : CMD_CONFIRMED_EVENT_REPORT
    length : 14
        {0x00 0x01 0x00 0x01 0x00 0x0e}
EventReportRes.
ManagedObjectId 
    m_obj_class : NOM_MOC_VMS_MDS
    context_id : 0
    handle : 0
RelativeTime 
    event_time : 4736768
OIDType 
    event_type : NOM_NOTI_MDS_CREAT
u_16 
    length : 0
        {0x00 0x21 0x00 0x00 0x00 0x00 0x00 0x48 0x47 0x00 0x0d 0x06 0x00 0x00} 

"""



