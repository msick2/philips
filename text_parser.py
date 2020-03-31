import sys







def text_Object_Classes():

    f = open("text_Object_Classes.txt", 'r')

    while True:

        line1 = f.readline()
        if not line1: break



        line2 = f.readline()
        if not line2: break

        line1 = line1.rstrip()
        line2 = line2.rstrip()

        line1 = line1.split(" ")


        new_line = f"{line1[0]} = {line1[1]} # {line2}"


        print(new_line)


    f.close()


def text_Numerics():
    f = open("text_Numerics.txt", 'r')

    while True:

        line = f.readline()
        if not line: break

        line = line.rstrip()

        if line.find(" 0x") != -1:

            lines = line.split(" ")
            new_line = f"{lines[0]} = {lines[1]}"
            print(new_line)
        #print(line)

    f.close()


def text_Enumerations():
    f = open("text_Enumerations.txt", 'r')

    while True:

        line = f.readline()

        if not line:
            break

        line = line.rstrip()

        lines = line.split(" ")

        num = len(lines)

        new_line = ""
        new_line += f"{lines[0]} = {lines[num-1]} # "

        n = 0

        for _ in range(num - 2):
            new_line += f"{lines[n + 1]} "
            n += 1

        #new_line = f"{lines[0]} = {lines[1]}"
        print(new_line)
        #print(line)

    f.close()


def text_Waves():
    f = open("text_Numerics.txt", 'r')

    while True:

        line = f.readline()
        if not line: break

        line = line.rstrip()

        if line.find(" 0x") != -1:

            lines = line.split(" ")
            new_line = f"{lines[0]} = {lines[1]}"
            print(new_line)
        #print(line)

    f.close()

def text_Attribute_IDs():
    f = open("text_Attribute_IDs.txt", 'r')


    while True:

        line1 = f.readline()
        if not line1: break

        line2 = f.readline()
        if not line2: break

        line1 = line1.rstrip()
        line2 = line2.rstrip()

        line2 = line2.split(" ")

        new_line = f"{line2[0]} = {line2[1]} # {line1}"

        print(new_line)


    f.close()



def text_Unit_Codes():
    f = open("text_Unit_Codes.txt", 'r')


    while True:

        line1 = f.readline()
        if not line1: break

        line2 = f.readline()
        if not line2: break

        line1 = line1.rstrip()
        line2 = line2.rstrip()

        line2 = line2.split(" ")

        new_line = f"{line2[0]} = {line2[1]} # {line1}"

        print(new_line)


    f.close()



def text_alert_source():
    f = open("text_alert_source.txt", 'r')

    while True:

        line1 = f.readline()
        if not line1:
            break

        line1 = line1.rstrip()
        line1 = line1.split(" ")
        new_line = f"{line1[0]} = {line1[1]}"
        print(new_line)

    f.close()


def m700_constants():
    f = open("m700_constants_.py", 'r')

    val_dict = dict()

    while True:

        line1 = f.readline()
        if not line1:
            break

        line1 = line1.rstrip()
        line1 = line1.split("#")

        comment = ""

        if len(line1) == 2:
            comment = line1[1]

        line1 = line1[0].rstrip()
        lines = line1.split("=")


        val_const = lines[0].rstrip()
        val_value = lines[1].rstrip()
        comment = comment.rstrip()

        value = int(val_value, 0)

        if val_const in val_dict.keys():
            if val_dict[val_const][0] == value:
                #print("같다.")
                pass
            else:
                print(f"다르다 = {val_dict[val_const][0]} : {value} ===================================================")
        else:
            val_dict[val_const] = [value, comment]

    for data in val_dict:
        print(f"{data} = {val_dict[data][0]}  #{val_dict[data][1]}")

        #new_line = f"{line1[0]} = {line1[1]}"
        #print(f"{val_const}:{value}")

    f.close()



def text_define():
    f = open("text_define.txt", 'r')

    while True:

        line1 = f.readline()
        if not line1:
            break

        line1 = line1.rstrip()
        line1 = line1.split("/*")
        comment = ""

        data = line1[0].split(" ")
        define = data[0]
        name = data[1]
        val = data[2]
        if len(line1) == 2:
            comment = line1[1].split("*/")[0]

        new_line = f"{name} = {val}  #{comment}"
        print(new_line)

    f.close()


def text_label():
    f = open("text_label.txt", 'r')

    while True:

        line1 = f.readline()
        if not line1:
            break

        line1 = line1.rstrip()
        line1 = line1.split("(")

        if len(line1) == 2:
            vals = line1[1].split(")")

            name = line1[0].rstrip()
            val = vals[0].rstrip()

            new_line = f"{name} = {val}"
            print(new_line)



    f.close()




def m700_Label_Mapping_Table_():
    f = open("m700_Label_Mapping_Table_.py", 'r')

    val_dict = dict()

    while True:

        line1 = f.readline()
        if not line1:
            break

        line1 = line1.rstrip()
        #print(line1)
        lines = line1.split("=")

        val_const = lines[0].rstrip()
        val_value = lines[1].rstrip()

        value = int(val_value, 0)

        if val_const in val_dict.keys():
            if val_dict[val_const] == value:
                #print("같다.")
                pass
            else:
                print(f"다르다 = {val_dict[val_const]} : {value} ===================================================")
        else:
            val_dict[val_const] = value

    for data in val_dict:
        print(f"{data} = {val_dict[data]} ")

        #new_line = f"{line1[0]} = {line1[1]}"
        #print(f"{val_const}:{value}")

    f.close()

# Private Unicode Characters
# 267 page

m700_Label_Mapping_Table_()
