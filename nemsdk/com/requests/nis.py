from ._client import send


def status(endpoint):
    url = endpoint + '/status'
    return send(url, 'GET')


def heartbeat(endpoint):
    url = endpoint + '/heartbeat'
    return send(url, 'GET')
