def to_signed32(n):
    n = n & 0xffffffff
    return n | (-(n & 0x80000000))


def to_micro_xem(value):
    return int(value * 1000000)


def to_macro_xem(value):
    return int(value // 1000000)
