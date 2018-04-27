import unittest
from nemsdk.crypto.key_pair import get_random_key_pair
from nemsdk.crypto.message import encrypt, decrypt
from test.helpers import random_string
import random
import re


class TestMessage(unittest.TestCase):
    def test_encrypt_and_decrypt(self):
        sk, pk = get_random_key_pair()
        sk2, pk2 = get_random_key_pair()

        message = random_string(n=random.randrange(40))
        encrypted = encrypt(sk, pk2, message)

        pattern = re.compile(r'[0-9a-f]+')
        self.assertRegex(encrypted, pattern)

        decrypted = decrypt(sk2, pk, encrypted)
        self.assertEqual(message, decrypted)


if __name__ == '__main__':
    unittest.main()
