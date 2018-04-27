from ._client import send


def announce(endpoint, request_announce):
    url = endpoint + '/transaction/announce'
    params = request_announce
    return send(url, 'POST', **params)
