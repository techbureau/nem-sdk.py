from ._client import send


def info(endpoint):
    url = endpoint + '/node/info'
    return send(url, 'GET')


def extended_info(endpoint):
    url = endpoint + '/node/extended-info'
    return send(url, 'GET')


def all_peers(endpoint):
    url = endpoint + '/node/peer-list/all'
    return send(url, 'GET')


def reachable_peers(endpoint):
    url = endpoint + '/node/peer-list/reachable'
    return send(url, 'GET')


def active_peers(endpoint):
    url = endpoint + '/node/peer-list/active'
    return send(url, 'GET')


def max_chain_height_of_active_peers(endpoint):
    url = endpoint + '/node/active-peers/max-chain-height'
    return send(url, 'GET')


def experiences(endpoint):
    url = endpoint + '/node/experiences'
    return send(url, 'GET')
