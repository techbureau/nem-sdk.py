# refs https://nemproject.github.io/#transaction-fees
import math
from .mosaic import MAX_MOSAIC_QUANTITY, XEM_SUPPLY, XEM_DIVISIBILITY
from .utils.convert import to_micro_xem

IMPORTANCE_TRANSFER_TX = 0.15


AGGRGATE_MODIFICATION_TX = 0.5


MULTISIG_TX = 0.15


MULTISIG_SIGNATURE_TX = 0.15


PROVISION_NAMESPACE_TX = 0.15

ROOT_NAMESPACE_PROVISIONING = 100


SUB_NAMESPACE_PROVISIONING = 10


MOSAIC_DEFINITION_CREATION_TX = 0.15


MOSAIC_SUPPLY_CHANGE_TX = 0.15


TRANSFERING_XEM_FACTOR = 0.05


def transfer(amount, message=None, mosaics=None):
    fee_sum = 0

    if mosaics:
        fee_sum += _mosaic(to_micro_xem(amount), mosaics)
    else:
        fee_sum += _transfer(amount)

    if (message is not None) and (len(message['payload']) > 0):
        fee_sum += _message(message['payload'])

    return round(fee_sum, 2)


def _transfer(amount):
    return TRANSFERING_XEM_FACTOR * min(max(1, amount // 10000), 25)


def _message(payload):
    msg_length = 0 if payload is None else len(payload.encode())
    if msg_length == 0:
        return 0
    else:
        return TRANSFERING_XEM_FACTOR * (msg_length // 2 // 32 + 1)


def _mosaic(amount, mosaics):
    if type(mosaics) is not list:
        mosaics = [mosaics]

    micro_amount = to_micro_xem(amount)
    fee_sum = 0
    for mosaic in mosaics:
        q = mosaic['quantity']
        s = mosaic['initialSupply']
        d = mosaic['divisibility']

        if d == 0 and s <= 10000:
            fee_sum += 1
            continue

        xem_equivalent = _calculate_xem_equivalent(micro_amount, q, s, d)
        xem_fee = min(max(1, xem_equivalent // 10000), 25)
        total_mosaic_quantity = s * (10 ** d)
        supply_related_adjustment = _calculate_supply_related_adjustment(total_mosaic_quantity)
        unweighted_fee = max(xem_fee - supply_related_adjustment, 1)
        fee_sum += unweighted_fee

    return round(fee_sum * TRANSFERING_XEM_FACTOR, 2)


def _calculate_xem_equivalent(micro_amount, quantity, supply, divisibility):
    if supply == 0:
        return 0
    else:
        return micro_amount * XEM_SUPPLY * quantity / supply / (10 ** (divisibility + XEM_DIVISIBILITY))


def _calculate_supply_related_adjustment(total_mosaic_quantity):
    return math.floor(0.8 * math.log(MAX_MOSAIC_QUANTITY / total_mosaic_quantity))
