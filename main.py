"""
- 시리얼 연결 후 시작신호가 오면 패킷을 보내면서 시작을 한다.

- 어떤 데이터를 요구 할 것인지를 확인하는 기능.
    - 체크박스 등의 방식으로 요청할 데이터를 선택하여 요청 및 수신한다.
    - 데이터를 요청 하는 방법(어떤 데이터를 요청하려면 패킷을 어떻게 보내야 하는지)
        - 실제 장비로 보내는 프로토콜은 요청하는 데이터 종류에 따라 주고받는 패킷이 다르다

- 프로그램 시작 시 요구하는 데이터 내용을 전달받고 시작한다.
    - 요구하는 데이터에 따라 장비로 보내는 패킷의 내용이 달라진다.
    - 시작 시 요구내용을 받고 그에 따라 패킷을 만들어 전송한다.

- 패킷을


- 시리얼통신을 하는 스레드
    - 송 수신을 하며 세션을 유지한다.


- 프로그램 시작 시 설정파일을 열어 내부 설정을 한다.
    - 카프카 IP
    - 장비와 연결될 통신포트
    - 장비로 요청할 데이터 리스트 (체크박스 타입)


- 프로그램 구동
    1. 시작 이후 기본 설정을 한다.
    2. 시리얼 통신 스레드에서 패킷을 하나 받는다
    3. 패킷을 분석
    4. 세션유지를 위한 패킷 전송 또는 카프카로 전송할 패킷 제작
    5. 카프카로 패킷 전송
    6. 2번부터 반복
    7. 종료시 종료 패킷 전송


- 시리얼 통신 스레드를 통해서 어떤 데이터를 받고 그 데이터는 스레드 밖에서 처리 할 수 있다.

"""

import json

def makeJsonInit():
    file_print = open("setting.json", "w")

    text_dict = dict()
    text_dict["KAFKA_IP"] = "123.234.123.12"
    text_dict["KAFKA_PORT"] = "12345"
    text_dict["MON_VALUE"] = dict()
    text_dict["MON_VALUE"]["EEG1"] = "X"
    text_dict["MON_VALUE"]["EEG2"] = "O"
    text_dict["MON_VALUE"]["EEG3"] = "X"
    text_dict["MON_VALUE"]["EEG4"] = "X"

    file_print.write(f"{json.dumps(text_dict)}\n")


def json_loading(filename):
    json_data = open(filename).read()
    ret_dict = json.loads(json_data)
    return ret_dict


def main():
    # todo : 기본설정파일 로딩 (JSON 텍스트 파일 형식)
    #makeJsonInit()
    dict_setting = json_loading("setting.json")
    print(dict_setting)

    # todo : 시리얼 통신 스레드를 연다.




if __name__ == "__main__":
    main()








