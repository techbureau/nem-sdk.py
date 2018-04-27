import nem_ed25519
from binascii import unhexlify


def encrypt(sk, recipient_pk, message):
    encrypted = nem_ed25519.encrypt(sk, recipient_pk, message.encode('utf8'))
    return encrypted.hex()


def decrypt(sk, recipient_pk, message):
    decrypted = nem_ed25519.decrypt(sk, recipient_pk, unhexlify(message))
    return decrypted.decode('utf8')
