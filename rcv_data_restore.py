import crcmod.predefined # pip install crcmod

calc_crc = crcmod.mkCrcFun(0x11021, rev=True, initCrc=0xffff)


def get_crc(data):
    checkSum = calc_crc(data)
    crcarray = (checkSum).to_bytes(2, byteorder='little')
    crc1 = bytearray(crcarray)
    return crc1


def complement(_data):
    retdata = bytearray()

    for index in range(len(_data)):
        retdata.append(_data[index] ^ 0xff)
    return retdata


def data_level0(data_):
    enable = False

    data = bytearray(data_)
    gd = bytearray()
    for index in range(len(data)):

        if enable:

            if data[index] == 0xc1:
                break

            else:
                gd.append(data[index])

        if data[index] == 0xc0:
            enable = True

    return gd


def data_level1(data_):
    data = bytearray(data_)
    gd = bytearray()

    flag_cvt = False

    for one in data:

        if flag_cvt:
            gd.append(one ^ 0x20)
            flag_cvt = False

        elif one == 0x7d:
            flag_cvt = True

        else:
            gd.append(one)

    return gd


def input_rcv_data(data):
    data_lv0 = data_level0(data)  # 0xc1과 0x7d를 다 뺀다.
    data_lv1 = data_level1(data_lv0)  # 0x7d를 고친다.
    crc_rcv = data_lv1[len(data_lv1) - 2: len(data_lv1)]  # 맨 마지막 2개를 얻음  [RCV CRC]
    crc_rcv_comp = complement(crc_rcv)  # 맨 마지막 2개를 반전  [comp RCV CRC]
    data_rcv = data_lv1[0: len(data_lv1) - 2]  # 맨 마지막 2개 빼고 모든 데이터 [RCV DATA]
    crc_calc = get_crc(data_rcv)  # 맨 마지막 2개 빼고 모든 데이터의 CRC [CALC CRC]
    crc_calc_comp = complement(crc_calc)  # 맨 마지막 2개 빼고 모든 데이터의 CRC의 반전 [comp CALC CRC]

    rcv_res = crc_rcv_comp[0] * 255 + crc_rcv_comp[1]
    calc_res = crc_calc[0] * 255 + crc_calc[1]

    # print("   INPUT DATA: " + ''.join('0x{:02x} '.format(x) for x in data))
    # print("    DATA LV 1: " + ''.join('0x{:02x} '.format(x) for x in data_lv1))
    # print("     RCV Data: " + ''.join('0x{:02x} '.format(x) for x in data_rcv))
    # print("      RCV CRC: " + ''.join('0x{:02x} '.format(x) for x in crc_rcv_comp))
    # print("RCV CRC COMPD: " + ''.join('0x{:02x} '.format(x) for x in crc_rcv))
    # print("     CALC CRC: " + ''.join('0x{:02x} '.format(x) for x in crc_calc))
    # print("CALC CRC COMP: " + ''.join('0x{:02x} '.format(x) for x in crc_calc_comp))
    # print(f"Rcv res: {rcv_res}")
    # print(f"Calc res: {calc_res}")

    if rcv_res == calc_res:
        return (True, data_rcv)

    return (False, data_rcv)
