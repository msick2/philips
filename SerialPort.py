import time
import threading
import json
import serial  # pip install pyserial
import rcv_data_restore
import receiver


class SerialPort:

    def __init__(self, port, baud, rcv_callback, send_thread):
        """
        시리얼포트와 보레이트를 받아 시리얼 객체를 생성한다.
        수신처리 함수와 송신처리 함수를 전달받아 스레드를 생성한다.
        :param port: 시리얼포트
        :param baud: 통신속도
        :param func_Rcv: 수신처리 함수
        :param func_Snd: 송신처리 함수
        """
        self.cSerialPort = serial.Serial(port, baud, timeout=0)
        self.rcv_callback = rcv_callback
        self.send_thread = send_thread

    def threading(self):
        thread_rcv = threading.Thread(target=self.thread_rcv)
        thread_snd = threading.Thread(target=self.send_thread)
        thread_rcv.start()
        thread_snd.start()

    def send_bytearray(self, data):
        self.cSerialPort.write(data)

    def send_dict(self, dict_data):
        self.cSerialPort.write(json.dumps(dict_data).encode('ascii'))

    # 수신받은 json 문자열을 dict로 변환
    def convert_json(self, strData):
        try:
            dataDict = json.loads(strData)
            return dataDict

        except json.decoder.JSONDecodeError as errors:
            print(f"JSON ERROR: {errors}")
            print(strData)
            return False

    # 수신받은 아스키문자열을 utf8로 변환
    def convert_utf8(self, byteArrayData):
        rcvArray = bytearray(len(byteArrayData))
        index = 0

        for temp in byteArrayData:
            rcvArray[index] = temp[0]
            index = index + 1

        return rcvArray.decode('utf-8')

    # 데이터를 수신받아 한 패킷이 완성되면 처리 한다.
    def thread_rcv(self):
        rcv_enable = False
        count = 0
        rcv_data_array = bytearray()
        c_parser = receiver.Parser()

        while True:
            if self.cSerialPort.inWaiting() != 0:  # 버퍼가 비어있지 않으면
                rcv_byte = self.cSerialPort.read(1)  # 버퍼에서 1바이트를 가져온다.

                if not rcv_enable:  # 수신 대기중이면
                    if rcv_byte == bytes(b'\xc0'):  # 수신 받은 문자가 시작문자 이면
                        rcv_data_array.append(rcv_byte[0])
                        rcv_enable = True  # 수신 상태로 전환

                else:  # 수신 중이면
                    rcv_data_array.append(rcv_byte[0])

                    if rcv_byte == bytes(b'\xc1'):  # 현재 문자가 종료뮨자 인지 확인
                        # 맞다면 패킷이 완료 된 것이므로 데이터를 처리 한다. ----------------------------------------------------
                        res = rcv_data_restore.input_rcv_data(rcv_data_array)

                        if res[0]:
                            data_dict = c_parser.input_data(res[1])  # 패킷을 분석하여 dict로 출력을 한다. 이것을 적절히 사용하면 된다.
                            self.rcv_callback(data_dict)

                        else:
                            print("PACKET ERROR")
                        # ----------------------------------------------------------------------------------------------
                        rcv_data_array = bytearray()
                        count += 1

                        rcv_enable = False  # 수신 대기 상태로 전환

            else:
                time.sleep(0.005)  # 버퍼가 비어있으면 슬립을 주어 스레드에 유휴 시간을 준다.


"""
cSerialPort = SerialPort("COM7", 115200)

cSerialPort.threading()

"""
