from nemsdk.com.requests.transaction import announce
from .serializer import serialize_tx
from nemsdk.crypto.key_pair import KeyPair


def send(entity, sk, endpoint):
    data = serialize_tx(entity)
    keypair = KeyPair(sk, entity['signer'])
    signature = keypair.sign(data)
    request_announce = {
        'data': data,
        'signature': signature
    }
    return announce(endpoint, request_announce)
