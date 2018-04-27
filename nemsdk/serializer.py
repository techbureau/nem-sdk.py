from binascii import unhexlify, hexlify
from nemsdk.tx_type import *


def serialize_tx(entity):
    common_part = _common_part(entity)

    if entity['type'] == TRANSFER:
        if entity.get('mosaics', None):
            tx_part = _transfer_tx2(entity)
        else:
            tx_part = _transfer_tx1(entity)

    elif entity['type'] == MULTISIG:
        tx_part = _multisig_tx(entity)
    elif entity['type'] == MULTISIG_SIGNATURE:
        tx_part = _multisig_signature_tx(entity)
    elif entity['type'] == MULTISIG_AGGREGATE_MODIFICATION_TRANSFER:
        tx_part = _multisig_aggregate_modification(entity)
    elif entity['type'] == PROVISION_NAMESPACE:
        tx_part = _provision_namespace(entity)
    else:
        tx_part = b''
    return hexlify(common_part + tx_part).decode()


def _common_part(entity):
    binary = b''
    binary += entity['type'].to_bytes(4, "little")
    binary += entity['version'].to_bytes(4, "little", signed=True)
    binary += entity['timeStamp'].to_bytes(4, "little")
    binary += int(32).to_bytes(4, "little")
    binary += unhexlify(entity['signer'].encode('utf8'))
    binary += entity['fee'].to_bytes(8, "little")
    binary += entity['deadline'].to_bytes(4, "little")
    return binary


def _transfer_tx1(entity):
    binary = b''
    binary += int(40).to_bytes(4, "little")
    binary += entity['recipient'].encode('utf8')
    binary += entity['amount'].to_bytes(8, "little")
    binary += _message(entity.get('message', None))
    return binary


def _transfer_tx2(entity):
    binary = b''
    binary += _transfer_tx1(entity)
    binary += _mosaics(entity)
    return binary


def _mosaics(entity):
    binary = b''
    mosaics = entity['mosaics']

    binary += len(mosaics).to_bytes(4, 'little')

    # need sort
    for mosaic in sorted(mosaics, key=lambda x: x['mosaicId']['namespaceId'] + x['mosaicId']['name']):

        quantity = mosaic['quantity'].to_bytes(8, "little")
        namespace_id = mosaic['mosaicId']['namespaceId'].encode('utf8')
        namespace_id_len = len(namespace_id).to_bytes(4, 'little')
        name = mosaic['mosaicId']['name'].encode('utf8')
        name_len = len(name).to_bytes(4, 'little')
        mosaic_id_structure = namespace_id_len + namespace_id + name_len + name
        mosaic_id_structure_len = len(mosaic_id_structure).to_bytes(4, "little")
        mosaic_structure = mosaic_id_structure_len + mosaic_id_structure + quantity
        mosaic_structure_len = len(mosaic_structure).to_bytes(4, "little")

        binary += mosaic_structure_len
        binary += mosaic_id_structure_len
        binary += namespace_id_len
        binary += namespace_id
        binary += name_len
        binary += name
        binary += quantity

    return binary


def _message(msg):
    binary = b''
    if (msg is None) or (msg.get('payload') is None) or (len(msg['payload']) == 0):
        binary += int(0).to_bytes(4, "little")
        return binary

    msg_length = len(unhexlify(msg['payload']))
    binary += int(msg_length + 8).to_bytes(4, "little")
    binary += msg['type'].to_bytes(4, "little")
    binary += msg_length.to_bytes(4, "little")
    binary += unhexlify(msg['payload'].encode('utf8'))

    return binary


def _multisig_tx(entity):
    binary = b''
    inner_tx = unhexlify(serialize_tx(entity['otherTrans']))
    binary += len(inner_tx).to_bytes(4, 'little')
    binary += inner_tx
    return binary


def _multisig_signature_tx(entity):
    binary = b''
    hash_length = len(unhexlify(entity['otherHash']['data'].encode('utf8')))
    binary += (hash_length + 4).to_bytes(4, 'little')
    binary += hash_length.to_bytes(4, 'little')

    binary += unhexlify(entity['otherHash']['data'].encode('utf8'))
    binary += int(40).to_bytes(4, "little")
    binary += entity['otherAccount'].encode('utf8')
    return binary


def _multisig_aggregate_modification(entity):
    binary = b''

    modifications = entity['modifications']
    binary += len(modifications).to_bytes(4, 'little')
    for modification in modifications:
        binary += int(40).to_bytes(4, 'little')
        binary += modification['modificationType'].to_bytes(4, 'little')
        binary += int(32).to_bytes(4, 'little')
        binary += unhexlify(modification['cosignatoryAccount'].encode('utf8'))

    if entity.get('minCosignatories'):
        binary += int(4).to_bytes(4, 'little')
        binary += entity['minCosignatories']['relativeChange'].to_bytes(4, 'little')

    return binary


def _provision_namespace(entity):
    binary = b''
    binary += int(40).to_bytes(4, 'little')
    binary += entity['rentalFeeSink'].encode('utf8')
    binary += entity['rentalFee'].to_bytes(8, 'little')
    binary += len(entity['newPart']).to_bytes(4, 'little')
    binary += entity['newPart'].encode('utf8')

    if entity['parent']:
        binary += len(entity['parent']).to_bytes(4, 'little')
        binary += entity['parent'].encode('utf8')
    else:
        binary += b'\xff\xff\xff\xff'
    return binary
