from nemsdk.crypto.message import encrypt
from binascii import hexlify

# TODO consider prepare_as_plain, prepare_as_encrypted method


class Message:
    def __init__(self, message, message_type=1):
        assert type(message) is str, "message must 'str' object"
        assert message_type in {1, 2}, 'message type must be 1 or 2'

        self.message = message
        self.message_type = message_type

    def prepare(self, sk=None, recipient_pk=None):
        if self.message_type == 1:
            return {'payload': hexlify(self.message.encode('utf8')).decode('utf8'), 'type': self.message_type}

        assert sk is not None, 'message type 2 requires secret key'
        assert recipient_pk is not None, 'message type 2 requires recipient public key'

        payload = encrypt(sk, recipient_pk, self.message)
        return {'payload': payload, 'type': self.message_type}
