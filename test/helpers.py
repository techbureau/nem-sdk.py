import string
import random


def random_string(n):
    chars = string.ascii_letters + string.digits
    s = ''
    return s.join([random.choice(chars) for _ in range(n)])
