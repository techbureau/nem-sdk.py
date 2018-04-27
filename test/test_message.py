import unittest
from nemsdk.message import Message
from nemsdk.crypto.key_pair import get_random_key_pair
import re


class TestMessage(unittest.TestCase):
    def test_message_is_string_type(self):
        Message('text')
        with self.assertRaises(AssertionError):
            Message(1)

    def test_message_type_is_1_or2(self):
        Message('text', message_type=1)
        Message('text', message_type=2)

        with self.assertRaises(AssertionError):
            Message('text', message_type=4)

    def test_plain_message(self):
        message = Message('message', message_type=1)
        self.assertDictEqual(message.prepare(), {'payload': '6d657373616765', 'type': 1})

    def test_encrypted_message_without_parameters(self):
        message = Message('message', message_type=2)
        with self.assertRaises(AssertionError):
            message.prepare(sk=None, recipient_pk='public_key')

        with self.assertRaises(AssertionError):
            message.prepare(sk='secret_key', recipient_pk=None)

    def test_message_encrypt(self):
        my_sk, my_pk = get_random_key_pair()
        recipient_sk, recipient_pk = get_random_key_pair()
        message = Message('plain text', message_type=2)

        msg = message.prepare(my_sk, recipient_pk)
        self.assertEqual(msg['type'], 2)
        pattern = re.compile(r'[0-9a-f]+')
        self.assertRegex(msg['payload'], pattern)


if __name__ == '__main__':
    unittest.main()
