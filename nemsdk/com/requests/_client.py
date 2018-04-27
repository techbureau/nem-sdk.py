import requests
import json


def send(url, method, **options):
    if method not in ['GET', 'POST']:
        raise ValueError('method must be in [GET, POST]')

    if method == 'GET':
        res = requests.get(url, params=options)
    else:
        res = requests.post(url, data=json.dumps(options), headers={'content-type': 'application/json'})

    return res.json() if res.text else None
