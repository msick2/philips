import time
import threading
import json
import serial # pip install pyserial


class SerialPort:

    def __init__(self, port, baud, func_Rcv, func_Snd):
        """
        시리얼포트와 보레이트를 받아 시리얼 객체를 생성한다.
        수신처리 함수와 송신처리 함수를 전달받아 스레드를 생성한다.
        :param port: 시리얼포트
        :param baud: 통신속도
        :param func_Rcv: 수신처리 함수
        :param func_Snd: 송신처리 함수
        """
        self.cSerialPort = serial.Serial(port, baud, timeout=0)
        self.func_Rcv = func_Rcv
        self.func_Snd = func_Snd

    def threading(self):
        threadRcv = threading.Thread(target=self.func_Rcv)
        threadSnd = threading.Thread(target=self.func_Snd)
        threadRcv.start()
        threadSnd.start()

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

    def thread_rcv(self):
        line = []
        rcvEnable = False
        rcvCount = 0

        while True:

            if self.cSerialPort.inWaiting() != 0:  # 버퍼가 비어있지 않으면

                n8Rcv = self.cSerialPort.read(1)  # 버퍼에서 1바이트를 가져온다.

                if not rcvEnable:  # 수신 대기중이면

                    if n8Rcv == bytes(b'$'):  # 수신 받은 문자가 { 이면
                        line.append(n8Rcv)  # 수신 받은 문자 저장
                        rcvEnable = True  # 수신 상태로 전환
                        rcvCount = 0
                else:  # 수신 중이면
                    line.append(n8Rcv)  # 수신 받은 문자 저장

                    rcvCount += 1

                    if rcvCount == 16:  # 16번째 바이트 인지
                        # 맞다면 패킷이 완료 된 것이므로 데이터를 처리 한다.
                        # dataLine = self.convertUtf8(line)
                        # dictRcv = self.convertJson(dataLine)

                        # ---------------------------------------------------------------------------------------------------------------------
                        # print (line)

                        #self.processWeather(line)

                        # ---------------------------------------------------------------------------------------------------------------------
                        del line[:]  # 데이터 저장 리스트 삭제
                        rcvEnable = False  # 수신 대기 상태로 전환

            else:
                time.sleep(0.005)  # 버퍼가 비어있으면 슬립을 주어 스레드에 유휴 시간을 준다.

