from ._client import send


def height(endpoint):
    url = endpoint + '/chain/height'
    return send(url, 'GET')


def score(endpoint):
    url = endpoint + '/chain/score'
    return send(url, 'GET')


def last_block(endpoint):
    url = endpoint + '/chain/last-block'
    return send(url, 'GET')


def block_by_height(endpoint, height):
    url = endpoint + '/block/at/public'
    params = {'height': height}
    return send(url, 'POST', **params)
