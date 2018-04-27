from nem_ed25519 import sign, public_key, secret_key, get_address  # TODO: remove this dependency if possible

from binascii import unhexlify, hexlify


class KeyPair:
    def __init__(self, hex_sk=None, hex_pk=None):
        self.sk = hex_sk or self.generate_secret_key()
        self._pk = hex_pk

    @property
    def pk(self):
        if not self._pk:
            self._pk = self.calculate_pk()
        return self._pk

    def sign(self, data):
        data_byte = unhexlify(data.encode('utf8'))
        sig = sign(msg=data_byte, sk=self.sk, pk=self.pk)
        return hexlify(sig).decode()

    def calculate_pk(self):
        return public_key(self.sk)

    def calculate_address(self, is_mainnet=True):
        return get_address(self.pk, main_net=is_mainnet)

    @staticmethod
    def generate_secret_key(seed=None):
        return secret_key(seed)


def get_random_key_pair():
    kp = KeyPair()
    return kp.sk, kp.pk


def get_random_account(is_mainnet=True):
    kp = KeyPair()
    sk, pk, address = kp.sk, kp.pk, kp.calculate_address(is_mainnet)
    return sk, pk, address
