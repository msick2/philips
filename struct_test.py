import ctypes
from ctypes import Structure, c_uint, c_ushort, c_uint8


class ABC(Structure):
    _pack_ = 1
    _fields_ = [("a", c_uint), ("b", c_ushort), ("c", c_ushort)]


class DEF(Structure):
    _pack_ = 1
    _fields_ = [("abc", ABC), ("i", c_uint8)]


def main():
    b = bytearray(b'\x88\x08\xc0\xf9\x02\x85\x10\x00\xcc')

    # check if bytearray can be applied to structure.
    if len(b) < ctypes.sizeof(DEF):
        print("error: bytearray is too short for DEF.")
        return

    s = DEF.from_buffer(b)
    print("abc.a: {:#x}".format(s.abc.a))
    print("abc.b: {:#x}".format(s.abc.b))
    print("abc.c: {:#x}".format(s.abc.c))
    print("i: {:#x}".format(s.i))

if __name__ == '__main__':
    main()