import ctypes
from ctypes import Structure, c_int8, c_int16, c_int32, c_uint8, c_uint16, c_uint32

import m700_struct
import m700_func
import rcv_data_restore
import data_computer
import data_monitor



def func_ROIV_APDU(ret_data):

    ret_data = m700_func.l2_ROIVapdu(ret_data)

    # print(f"| ROIVapdu.invoke_id   : {ret_data['ROIVapdu']['invoke_id']}")
    # print(f"| ROIVapdu.command_type: {ret_data['ROIVapdu']['command_type']}")
    # print(f"| ROIVapdu.length      : {ret_data['ROIVapdu']['length']}")

    if ret_data['ROIVapdu']['command_type'] == m700_struct.CMD_EVENT_REPORT:
        # CMD_EVENT_REPORT: An Event Report is used for an unsolicited event message.
        ret_data = m700_func.l3_EventReportArgument(ret_data)

        print(f"| EventReportArgument.managed_object   : {ret_data['EventReportArgument']['managed_object']}")
        print(f"| EventReportArgument.event_time: {ret_data['EventReportArgument']['event_time']}")
        print(f"| EventReportArgument.event_type      : {ret_data['EventReportArgument']['event_type']}")
        print(f"| EventReportArgument.length      : {ret_data['EventReportArgument']['length']}")

        pass

    elif ret_data['ROIVapdu']['command_type'] == m700_struct.CMD_CONFIRMED_EVENT_REPORT:
        # CMD_CONFIRMED_EVENT_REPORT: The Confirmed Event Report is an unsolicited event
        # message for which the receiver must send an Event Report Result message.
        print(f"| CMD_CONFIRMED_EVENT_REPORT")
        pass

    elif ret_data['ROIVapdu']['command_type'] == m700_struct.CMD_GET:
        # CMD_GET: The Get operation is used to request attribute values of managed objects. The receiver
        # responds with a Get Result message.
        print(f"| CMD_GET")

        pass

    elif ret_data['ROIVapdu']['command_type'] == m700_struct.CMD_SET:
        # CMD_SET: The Set operation is used to set values of managed objects.
        print(f"| CMD_SET")

        pass

    elif ret_data['ROIVapdu']['command_type'] == m700_struct.CMD_CONFIRMED_SET:
        # CMD_CONFIRMED_SET: The Confirmed Set operation is used to set attribute values of
        # managed objects. The receiver responds with a Set Result message.
        print(f"| CMD_CONFIRMED_SET")

        pass

    elif ret_data['ROIVapdu']['command_type'] == m700_struct.CMD_CONFIRMED_ACTION:
        # CMD_CONFIRMED_ACTION: The Confirmed Action is a message to invoke an activity on the
        # receiver side. The receiver must send an Action Result message.
        print(f"| CMD_CONFIRMED_ACTION")

        pass





def func_RORS_APDU(ret_data):
    # 모니터 장비에서 수신되는 데이터의 대부분이 이 타입이다.
    '''
------------------------------------------------------------------------------------------------------------------------
    MDSCreateEventResult ::=
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
------------------------------------------------------------------------------------------------------------------------
    MDSPollActionResult ::=
        <SPpdu>
        <ROapdus
            ro_type := RORS_APDU
        <RORSapdu
            invoke_id := "mirrored from request message"
            command_type := CMD_CONFIRMED_ACTION 7
        <ActionResult
            managed_object := {NOM_MOC_VMS_MDS, 0, 0},
            action_type := NOM_ACT_POLL_MDIB_DATA
        <PollMdibDataReply>
------------------------------------------------------------------------------------------------------------------------
    MDSPollActionResultExt ::=
        <SPpdu>
        <ROapdus>
            ro_type := RORS_APDU
        <RORSapdu>
            invoke_id := "mirrored from request message"
            command_type := CMD_CONFIRMED_ACTION 7
        <ActionResult>
            managed_object := {NOM_MOC_VMS_MDS, 0, 0},
            action_type := NOM_ACT_POLL_MDIB_DATA_EXT
        <PollMdibDataReplyExt>
------------------------------------------------------------------------------------------------------------------------
    MDSGetPriorityListResult ::=
        <SPpdu>
        <ROapdus >
            ro_type := RORS_APDU
        <RORSapdu>
            invoke_id := “mirrored from request message”,
            command_type := CMD_GET 3
        <GetResult>
            managed_object := {NOM_MOC_VMS_MDS, 0, 0}
------------------------------------------------------------------------------------------------------------------------
    MDSSetPriorityListResult ::=
        <SPpdu>
        <ROapdus>
            ro_type := RORS_APDU
        <RORSapdu>
            invoke_id := “mirrored from request message”,
            command_type := CMD_CONFIRMED_SET 5
        <SetResult>
            managed_object := {NOM_MOC_VMS_MDS, 0, 0}
------------------------------------------------------------------------------------------------------------------------

    '''


    ret_data = m700_func.l2_RORSapdu(ret_data)


    print(f"| RORSapdu.invoke_id   : {ret_data['RORSapdu']['invoke_id']}")
    print(f"| RORSapdu.command_type: {ret_data['RORSapdu']['command_type']}")
    print(f"| RORSapdu.length      : {ret_data['RORSapdu']['length']}")



    ret_data = m700_func.l3_EventReportResult(ret_data)



    #print(f"| EventReportResult.managed_object : {ret_data['EventReportResult']['managed_object']}")
    #print(f"| EventReportResult.current_time   : {ret_data['EventReportResult']['current_time']}")
    #print(f"| EventReportResult.event_type     : {ret_data['EventReportResult']['event_type']}")
    #print(f"| EventReportResult.length         : {ret_data['EventReportResult']['length']}")



    if ret_data['RORSapdu']['command_type'] == m700_struct.CMD_EVENT_REPORT:

        print(f"| tail      : {ret_data['tail']}")

    elif ret_data['RORSapdu']['command_type'] == m700_struct.CMD_CONFIRMED_EVENT_REPORT:

        print(f"| tail      : {ret_data['tail']}")

    elif ret_data['RORSapdu']['command_type'] == m700_struct.CMD_GET:

        print(f"| tail      : {ret_data['tail']}")

    elif ret_data['RORSapdu']['command_type'] == m700_struct.CMD_SET:

        print(f"| tail      : {ret_data['tail']}")

    elif ret_data['RORSapdu']['command_type'] == m700_struct.CMD_CONFIRMED_SET:

        print(f"| tail      : {ret_data['tail']}")

    elif ret_data['RORSapdu']['command_type'] == m700_struct.CMD_CONFIRMED_ACTION:
        # <ActionResult>

        ret_data = m700_func.l4_ActionResult(ret_data)

        print(f"| ActionResult.managed_object      : {ret_data['ActionResult']['managed_object']}")
        print(f"| ActionResult.action_type      : {ret_data['ActionResult']['action_type']}")
        print(f"| ActionResult.length      : {ret_data['ActionResult']['length']}")


        # <PollMdibDataReply>

        print(f"| tail      : {ret_data['tail']}")



def func_ROER_APDU(dict_data):
    pass


def func_ROLRS_APDU(dict_data):
    pass














ok = 0
nok = 1

for data in data_monitor.datas1:
#for data in data_computer.datas1:

    # print(data_computer.data)

    res = rcv_data_restore.input_rcv_data(data)

    if res[0]:
        # print(res[1])
        ok += 1

        #        s = m700_struct.Header_Common.from_buffer(res[1])

        ret_data = m700_func.l0_FrameHdr(res[1])
        ret_data = m700_func.l1_SPpdu(ret_data)
        ret_data = m700_func.l1_ROapdus(ret_data)

        print(f"+============================")
        #print(f"| FrameHdr.protocol_id : {ret_data['FrameHdr']['protocol_id']}")
        #print(f"| FrameHdr.msg_type    : {ret_data['FrameHdr']['msg_type']}")
        #print(f"| FrameHdr.length      : {ret_data['FrameHdr']['length']}")
        #print(f"+----------------------------")
        #print(f"| SPpdu.session_id     : {ret_data['SPpdu']['session_id']:x}")
        #print(f"| SPpdu.p_context_id   : {ret_data['SPpdu']['p_context_id']:x}")
        #print(f"+----------------------------")
        #print(f"| ROapdus.ro_type      : {ret_data['ROapdus']['ro_type']}")
        #print(f"| ROapdus.length       : {ret_data['ROapdus']['length']}")

        # 일단 패킷을 여기까지는 공통으로 까고 이후에 SPpdu.session_id값이 0xe100인지 확인한다.

        if ret_data['SPpdu']['session_id'] == 0xe100:
            # 그 다음에 ROapdus.ro_type이 뭔지에 따라 나눠진다.
            if ret_data['ROapdus']['ro_type'] == m700_struct.ROIV_APDU:
                # (ROIV_APDU) invokes (calls) a remote operation.
                print(f"| RORS_APDU 0")
                func_ROIV_APDU(ret_data)


            elif ret_data['ROapdus']['ro_type'] == m700_struct.RORS_APDU:
                # (RORS_APDU) returns the result of a remote operation
                print(f"| RORS_APDU 1")
                func_RORS_APDU(ret_data)


            elif ret_data['ROapdus']['ro_type'] == m700_struct.ROER_APDU:
                # (ROER_APDU) returns an error for a remote operation.
                print(f"| ROER_APDU 2")
                func_ROER_APDU(ret_data)


            elif ret_data['ROapdus']['ro_type'] == m700_struct.ROLRS_APDU:
                # (ROLRS_APDU) returns parts of the result of a remote operation.
                # It is used when the size of the complete result exceeds the maximum size of one message.
                print(f"| ROLRS_APDU 3")
                func_ROLRS_APDU(ret_data)




        else:
            print("ACCESS 관련일듯")

        # define ROIV_APDU 1
        # define RORS_APDU 2
        # define ROER_APDU 3
        # define ROLRS_APDU 5

    #        str_type = "None"
    #
    #        if s.ROapdus.ro_type == 1:
    #            str_type = "ROIV_APDU"
    #        elif s.ROapdus.ro_type == 2:
    #            str_type = "RORS_APDU"
    #        elif s.ROapdus.ro_type == 3:
    #            str_type = "ROER_APDU"
    #        elif s.ROapdus.ro_type == 5:
    #            str_type = "ROLRS_APDU"

    #        print(f"+============================")
    #        print(f"| FrameHdr.protocol_id : {s.FrameHdr.protocol_id}")
    #        print(f"| FrameHdr.msg_type    : {s.FrameHdr.msg_type}")
    #        print(f"| FrameHdr.length      : {s.FrameHdr.length}")
    #        print(f"+----------------------------")
    #        print(f"| SPpdu.session_id     : {s.SPpdu.session_id:x}")
    #        print(f"| SPpdu.p_context_id   : {s.SPpdu.p_context_id}")
    #        print(f"+----------------------------")
    #        print(f"| ROapdus.ro_type      : {s.ROapdus.ro_type} - {str_type}")
    #        print(f"| ROapdus.length       : {s.ROapdus.length}")
    #        if s.ROapdus.ro_type == 2:
    #            s = m700_struct.MDSCreateEventResult.from_buffer(res[1])
    #            print(f"+----------------------------")
    #            print(f"| EventReportResult.managed_object.m_obj_class           : {s.EventReportResult.managed_object.m_obj_class}")
    #            print(f"| EventReportResult.managed_object.m_obj_inst.context_id : {s.EventReportResult.managed_object.m_obj_inst.context_id}")
    #            print(f"| EventReportResult.managed_object.m_obj_inst.handle     : {s.EventReportResult.managed_object.m_obj_inst.handle}")
    #            print(f"| EventReportResult.current_time                         : {s.EventReportResult.current_time}")
    #            print(f"| EventReportResult.event_type                           : {s.EventReportResult.event_type}")
    #            print(f"| EventReportResult.length                               : {s.EventReportResult.length}")

    else:
        # print(res[1])
        nok += 1

print("+----------------------------")
print(f"| ok:{ok}, nok:{nok}, {ok * 100 / (ok + nok):3.5}%")
print("+----------------------------")

"""
    # print(data_computer.data)

    res = rcv_data_restore.input_rcv_data(data)

    if res[0]:
        # print(res[1])
        ok += 1

        s = m700_struct.Header_Common.from_buffer(res[1])
        # define ROIV_APDU 1
        # define RORS_APDU 2
        # define ROER_APDU 3
        # define ROLRS_APDU 5

        str_type = "None"

        if s.ROapdus.ro_type == 1:
            str_type = "ROIV_APDU"
        elif s.ROapdus.ro_type == 2:
            str_type = "RORS_APDU"
        elif s.ROapdus.ro_type == 3:
            str_type = "ROER_APDU"
        elif s.ROapdus.ro_type == 5:
            str_type = "ROLRS_APDU"

        print(f"+============================")
        print(f"| FrameHdr.protocol_id : {s.FrameHdr.protocol_id}")
        print(f"| FrameHdr.msg_type    : {s.FrameHdr.msg_type}")
        print(f"| FrameHdr.length      : {s.FrameHdr.length}")
        print(f"+----------------------------")
        print(f"| SPpdu.session_id     : {s.SPpdu.session_id:x}")
        print(f"| SPpdu.p_context_id   : {s.SPpdu.p_context_id}")
#        print(f"+----------------------------")
#        print(f"| ROapdus.ro_type      : {s.ROapdus.ro_type} - {str_type}")
#        print(f"| ROapdus.length       : {s.ROapdus.length}")
#        if s.ROapdus.ro_type == 2:
#            s = m700_struct.MDSCreateEventResult.from_buffer(res[1])
#            print(f"+----------------------------")
#            print(f"| EventReportResult.managed_object.m_obj_class           : {s.EventReportResult.managed_object.m_obj_class}")
#            print(f"| EventReportResult.managed_object.m_obj_inst.context_id : {s.EventReportResult.managed_object.m_obj_inst.context_id}")
#            print(f"| EventReportResult.managed_object.m_obj_inst.handle     : {s.EventReportResult.managed_object.m_obj_inst.handle}")
#            print(f"| EventReportResult.current_time                         : {s.EventReportResult.current_time}")
#            print(f"| EventReportResult.event_type                           : {s.EventReportResult.event_type}")
#            print(f"| EventReportResult.length                               : {s.EventReportResult.length}")


    else:
        # print(res[1])
        nok += 1

print("+----------------------------")
print(f"| ok:{ok}, nok:{nok}, {ok * 100 / (ok + nok):3.5}%")
print("+----------------------------")



"""

'''
패킷을 받아서 맨 처음꺼 부터 까면서 하나하나 내려오는 방식으로 패킷을 분석한다.

하나를 까고 그것과 나머지를 리턴하도록 한다.
리스트 방식을 그것의 리스트를 리턴하도록 한다.
방식은 딕셔너리를 사용한다.

딕셔너리가 리턴되는데
클래스명과 그 객체
어레이와 나머지 데이터 로 들어온다.


크게 두가지 타입이 있음
데이터와 연결관련



'''
