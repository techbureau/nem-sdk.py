from ._client import send


_ACCOUNT_PATH = '/account'


def data(endpoint, address):
    url = endpoint + _ACCOUNT_PATH + '/get'
    params = {'address': address}
    return send(url, 'GET', **params)


def data_from_public_key(endpoint, public_key):
    url = endpoint + _ACCOUNT_PATH + '/get/from-public-key'
    params = {'publicKey': public_key}
    return send(url, 'GET', **params)


def forwarded(endpoint, address):
    url = endpoint + _ACCOUNT_PATH + '/get/forwarded'
    params = {'address': address}
    return send(url, 'GET', **params)


def forwarded_from_public_key(endpoint, public_key):
    url = endpoint + _ACCOUNT_PATH + '/get/forwarded/from-public-key'
    params = {'publicKey': public_key}
    return send(url, 'GET', **params)


def status(endpoint, address):
    url = endpoint + _ACCOUNT_PATH + '/status'
    params = {'address': address}
    return send(url, 'GET', **params)


def incoming_transactions(endpoint, address, txhash=None, txid=None):
    url = endpoint + _ACCOUNT_PATH + '/transfers/incoming'
    params = {
        'address': address,
        'hash': txhash,
        'id': txid,
    }
    return send(url, 'GET', **params)


def outgoing_transactions(endpoint, address, txhash=None, txid=None):
    url = endpoint + _ACCOUNT_PATH + '/transfers/outgoing'
    params = {
        'address': address,
        'hash': txhash,
        'id': txid,
    }
    return send(url, 'GET', **params)


def all_transactions(endpoint, address, txhash=None, txid=None):
    url = endpoint + _ACCOUNT_PATH + '/transfers/all'
    params = {
        'address': address,
        'hash': txhash,
        'id': txid,
    }
    return send(url, 'GET', **params)


def unconfirmed_transactions(endpoint, address):
    url = endpoint + _ACCOUNT_PATH + '/unconfirmedTransactions'
    params = {'address': address}
    return send(url, 'GET', **params)


def harvested_blocks(endpoint, address):
    url = endpoint + _ACCOUNT_PATH + '/harvests'
    params = {'address': address}
    return send(url, 'GET', **params)


# TODO: include `id`, `pageSize` parameters
def namespaces_owned(endpoint, address, parent=''):
    url = endpoint + _ACCOUNT_PATH + '/namespace/page'
    params = {'address': address, 'parent': parent}
    return send(url, 'GET', **params)


def mosaic_definitions_created(endpoint, address, parent=''):
    url = endpoint + _ACCOUNT_PATH + '/mosaic/definition/page'
    params = {'address': address, 'parent': parent}
    return send(url, 'GET', **params)


def mosaic_definitions(endpoint, address):
    url = endpoint + _ACCOUNT_PATH + '/mosaic/owned/definition'
    params = {'address': address}
    return send(url, 'GET', **params)


def mosaic_owned(endpoint, address):
    url = endpoint + _ACCOUNT_PATH + '/mosaic/owned'
    params = {'address': address}
    return send(url, 'GET', **params)


def start_harvesting(endpoint, private_key):
    url = endpoint + _ACCOUNT_PATH + '/unlock'
    params = {'value': private_key}
    return send(url, 'POST', **params)


def stop_harvesting(endpoint, private_key):
    url = endpoint + _ACCOUNT_PATH + '/lock'
    params = {'value': private_key}
    return send(url, 'POST', **params)


def unlock_info(endpoint):
    url = endpoint + _ACCOUNT_PATH + '/unlocked/info'
    return send(url, 'POST')


def historical_data(endpoint, address, startheight, endheight, increment):
    url = endpoint + _ACCOUNT_PATH + '/historical/get'
    params = {
        'address': address,
        'startHeight': startheight,
        'endHeight': endheight,
        'increment': increment,
    }
    return send(url, 'GET', **params)
