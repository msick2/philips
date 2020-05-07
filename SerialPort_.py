

"""
    기상측정장비

    9600bps



"""


import time
import json
import SerialPort

class EquipWeather(SerialPort.SerialPortBase):


    # Singleton ---------------------------------------------------
    _instance = None

    @classmethod
    def _getInstance(cls):
        return cls._instance

    @classmethod
    def instance(cls, serialPort, storage):
        if cls._instance is None:
            cls._instance = EquipWeather(serialPort, storage)
        return cls._instance
    # -------------------------------------------------------------



    def init(self):
        pass

    # 시리얼 수신 스레드
    def serialRcv_Main(self):
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
                        #dataLine = self.convertUtf8(line)
                        #dictRcv = self.convertJson(dataLine)

# ---------------------------------------------------------------------------------------------------------------------
                        #print (line)

                        self.processWeather(line)

# ---------------------------------------------------------------------------------------------------------------------
                        del line[:]  # 데이터 저장 리스트 삭제
                        rcvEnable = False  # 수신 대기 상태로 전환

            else:
                time.sleep(0.005)  # 버퍼가 비어있으면 슬립을 주어 스레드에 유휴 시간을 준다.


    listSendData = []



    def processWeather(self, datalist):
        intList = []

        for index in range(0, len(datalist)):
            intList.append(int.from_bytes(datalist[index], "big"))

        # -----------------------------
        # 풍향
        windDir = intList[2] + ((intList[3] & 0x10) >> 4)


        # -----------------------------
        # 온도
        temper = ((intList[4] | ((intList[3] & 0x07) << 8)) - 400) / 10.0

        # -----------------------------
        # 습도
        humidity = intList[5]

        # -----------------------------
        # 픙속
        windSpd = intList[6]


        # -----------------------------
        # 순간풍속
        gustSpd = intList[7]


        # -----------------------------
        # 강우량
        rainFall = (intList[8] << 8) + intList[9]

        # -----------------------------
        # 자외선
        UV = (intList[10] << 8) + intList[11]


        # -----------------------------
        # 조도
        LIGHT = (intList[12] << 24) + (intList[13] << 16) + (intList[14] << 8) + intList[15]



        self.cStorage.weatWindDir = windDir
        self.cStorage.weatTemper = temper
        self.cStorage.weatHumidity = humidity
        self.cStorage.weatWindSpd = windSpd
        self.cStorage.weatGustSpd = gustSpd
        self.cStorage.weatRainFall = rainFall
        self.cStorage.weatUV = UV
        self.cStorage.weatLIGHT = LIGHT


