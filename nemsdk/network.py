from nemsdk.utils.convert import to_signed32
import random


MAINNET_RENTAL_FEE_SINK = 'NAMESPACEWH4MKFMBCVFERDPOOP4FK7MTBXDPZZA'
TESTNET_RENTAL_FEE_SINK = 'TAMESPACEWH4MKFMBCVFERDPOOP4FK7MTDJEYP35'


def get_random_endpoint(port=7890):
    # TODO: add at any time
    nodes = [
        'http://alice2.nem.ninja',
        'http://alice3.nem.ninja',
        'http://alice4.nem.ninja',
        'http://alice5.nem.ninja',
        'http://alice6.nem.ninja',
        'http://alice7.nem.ninja',
        'http://alice8.nem.ninja',
        'http://alice9.nem.ninja',
    ]
    return random.choice(nodes) + ':' + str(port)


def get_version(tx_v, network):
    assert network in {'mainnet', 'testnet', 'mijin'}

    if network == 'mainnet':
        network_id = 0x68000000  # TODO: use constant
    elif network == 'testnet':
        network_id = 0x98000000
    else:
        network_id = 0x60000000
    return to_signed32(network_id + tx_v)


def get_rental_fee_sink(network):
    assert network in {'mainnet', 'testnet'}  # mijin?

    if network == 'mainnet':
        return MAINNET_RENTAL_FEE_SINK
    else:
        return TESTNET_RENTAL_FEE_SINK
